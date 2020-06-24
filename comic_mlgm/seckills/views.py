import json
import time
from datetime import timedelta
from redis import Redis

from alipay import AliPay
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from django.views import View
from django_redis import get_redis_connection
from django.conf import settings

from .models import *
from user.models import *
from utils.logging_dec import logging_check

# Create your views here.

"""
还未接入用户测试
"""

app_private_key_string = open(f'{settings.ALIPAY_KEY_DIRS}/app_private_key.pem').read()
alipay_public_key_string = open(f'{settings.ALIPAY_KEY_DIRS}/alipay_public_key.pem').read()
r = get_redis_connection('default')  # type:Redis


def crontab(seckill_price, seckill_time, continue_time, count, month):
    """
    当在admin界面创建或者修改秒杀表数据的时候，将调用该函数，在redis中存入该次秒杀的开启时间，价格，和门票总数,和商品总数
    :param seckill_price: 价格
    :param seckill_time: 开启时间
    :param continue_time: 持续时间
    :param count: 商品总数
    :param month: VIP月数（商品详情）
    """
    r.delete('seckills')
    time_now = (seckill_time - timezone.now()).seconds + continue_time
    cache.set('seckill_price', seckill_price, time_now)
    cache.set('seckill_time', seckill_time, time_now)
    cache.set('seckill_continue_time', continue_time, time_now)
    cache.set('seckill_count', count, time_now)
    cache.set('seckill_month', month, time_now)
    r.lpush('seckill_back', 1)  # 数据回收状态:有值，未回收，无值，已回收
    with r.pipeline(transaction=True) as pipe:
        pipe.multi()
        for i in range(count * 10):
            pipe.rpush('seckills', 0) if i % 5 else pipe.rpush('seckills', 1)
        pipe.expire('seckills', time_now)
        pipe.execute()


class MyAliPay(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 初始化alipay
        self.alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type='RSA2',
            debug=True  # 默认是False，True是请求转发到沙箱
        )

    def get_trade_url(self, order_id, price):
        # 生成支付宝支付连接  https://openapi.alipaydev.com/gateway.do? +查询字符串
        # 拼接查询字符串的函数
        query_str = self.alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=price,
            subject=f'达达商城:{order_id}',  # 对订单的描述
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=settings.ALIPAY_NOTIFY_URL,
        )
        return f'https://openapi.alipaydev.com/gateway.do?{query_str}'

    def get_verify_result(self, data, sign):
        # 调用支付宝验签，返回 bool 值
        return self.alipay.verify(data, sign)

    def get_trade_result(self, order_id):
        # 查询支付结果
        reslut = self.alipay.api_alipay_trade_query(order_id)
        print('-----------:', reslut)
        return True if reslut.get('trade_status') == 'TRADE_SUCCESS' else False


class Seckill(MyAliPay):

    @logging_check
    def get(self, request: WSGIRequest):
        """
        具体逻辑，先验正token，再验证请求是否在开启时间内，再验证用户当前秒杀次数是否超限，再发放门票作请求分离，只允许拿到门票的用户（110）进入支付页面
        """
        # 验证是否在活动开启时间内
        print('=======时间验证开始')
        try:
            if not cache.get('seckill_time') <= timezone.now() <= cache.get('seckill_time') + timedelta(
                    seconds=cache.get('seckill_continue_time')):
                return JsonResponse({'code': 10024, 'error': '时间未到了个喵'})
        except:
            print('=======时间验证失败')
            return JsonResponse({'code': 10024, 'error': '时间未到了个喵'})
        print('=======时间验证完毕')
        # 验证该用户对该次秒杀的请求总次数,暂定为10次
        try:
            print('进入秒杀次数加1')
            x = r.hincrby('seckill_count', f'{request.myuser.id}', 1)
            print(x)
            if x >= 20:
                return JsonResponse({'code': 10022, 'error': '抢购次数超限'})
        except Exception as e:
            print('错误：',e)
        print('==================次数加1完成,，开始验证门票')

        # 验证是否已经取得过门票
        tickes = r.hget('seckill_buff', f'{request.myuser.id}')
        if (not tickes) or tickes == b'100':
            if not r.hexists('seckill_order_id', f'{request.myuser.id}'):
                r.hset('seckill_order_id', f'{request.myuser.id}', time.time())
            number = int(r.lpop('seckills').decode())
            if number:
                r.hset('seckill_buff', f'{request.myuser.id}', 110)
                return JsonResponse({'code': 200,
                                     'url': self.get_trade_url(
                                         r.hget('seckill_order_id', f'{request.myuser.id}').decode(),
                                         int(cache.get('seckill_price')))})
            else:
                r.hset('seckill_buff', f'{request.myuser.id}', 100)
                return JsonResponse({'code': 10020, 'error': '没抢到了个喵'})
        if tickes == b'111':
            return JsonResponse({'code': 10021, 'error': '已经买过了'})
        if tickes == b'110':
            return JsonResponse(
                {'code': 200, 'url': self.get_trade_url(r.hget('seckill_order_id', f'{request.myuser.id}').decode(),
                                                        int(cache.get('seckill_price')))})


def seckill_time(request):
    """
    客户端请求当前秒杀时间
    """
    # time = timezone.now() + timedelta(days=30)
    try:
        timeout = cache.get('seckill_time') - timezone.now()  # type:timedelta

        print(timeout)
    except TypeError:
        return JsonResponse({'code': 10024})

    if not timeout.days or timeout.days == -1:
        if timeout > timedelta(seconds=0):
            return JsonResponse(
                {'code': 200, 'timeout': timeout.seconds, 'continue_time': cache.get('seckill_continue_time')})
        else:
            __time = timeout + timedelta(seconds=cache.get('seckill_continue_time'))
            return JsonResponse({'code': 200, 'timeout': 1, 'continue_time': __time.seconds}) if __time > timedelta(
                seconds=0) else JsonResponse({'code': 10025, 'error': '时间已经过了'})
    else:
        return JsonResponse({'code': 10023, 'error': '时间还早了个喵'})


class ResultView(MyAliPay):
    # 支付后重定向操作
    # 请求网址:http://127.0.0.1:8000/payment/result?
    # charset=utf-8&
    # out_trade_no=20191118213156027444&
    # method=alipay.trade.page.pay.return&
    # total_amount=999.00&sign=UFf0Qx1pjamQK%2F1BOz7%2BF0ZZaj77mNpX2cKb%2BV90J%2BNnNVIAtXJcVDqOtF5kDEhRey%2FlDgpNdQTktzWriF3r9KypI0hMvIKcwl8oXNLCO%2BXHXTKKKXfnsB0shW9SPrPuXCFC5V71c0bRQzT3%2BZsqKzS2pKqLQAZwTi6kBOiRzTpoJ3gcHMTumRENFRAPyvygclEvBRcsrwALVNUWhYEOfEV2%2BtL9E96tBLekGjS35ze%2F1J35KtX%2BySFhOo%2BiiEIHGbQvIDcmFTyKbGrlLjzEbQC1YGr5pzKo4MLuFMGmVDf9lAIqImDUmKplB%2BQpSiDBi8ZJADfd%2F2HfQkRkbCiLcA%3D%3D&
    # trade_no=2020060122001479280504494708&
    # auth_app_id=2016102200735655&version=1.0&
    # app_id=2016102200735655&
    # sign_type=RSA2&
    # seller_id=2088102180586012&
    # timestamp=2020-06-01+17%3A29%3A01
    @logging_check
    def get(self, request):
        request_data = {k: request.GET[k] for k in request.GET.keys()}
        sign = request_data.pop('sign')
        # 把公钥取出来和剩余的数据做验签
        is_verify = self.get_verify_result(request_data, sign)
        if not is_verify:
            return HttpResponse('违法访问')
        # 验签成功后，需要去数据库查看订单状态
        order_id = request_data['out_trade_no']
        if r.hget('seckill_buff',f'{request.myuser.id}') == b'111':
            return HttpResponseRedirect('http://127.0.0.1:8000/index')
        # 数据库订单状态没改，说明图里第7步(下面的post函数)出现问题
        # 主动向支付宝询问该订单支付状态
        result = self.get_trade_result(order_id)
        if not result:
            return HttpResponse('支付失败')
        user = Users.objects.get(id=request.userid),
        user.vip = timezone.now() + timedelta(
            days=31 * cache.get('seckill_month')) if user.vip <= timezone.now() else user.vip + timedelta(
            days=31 * cache.get('seckill_month'))
        r.hset('seckill_buff', f'{request.myuser.id}',111)
        return HttpResponseRedirect('http://127.0.0.1:8000/index')

    def post(self, request):
        # 此函数所有响应都是发给支付宝的，对用户的行为处理不能写进响应
        # 表单数据取出来，验签
        # 验证成功后， 校验交易状态，根据状态，修改订单状态
        # 这个速度比较块
        print('收到支付宝响应')
        json_obj = json.loads(request.body)
        sign = json_obj.pop('sign')
        is_verify = self.get_verify_result(json_obj, sign)
        if not is_verify:  # 验签
            print('++++++++++++++++++++++支付宝回函:验签错误')
            return HttpResponse('success')
        if json_obj['alipay_trade_pay_response']['receipt_amount'] != cache.get('seckill_price'):  # 验订单金额
            print('++++++++++++++++++++++支付宝回函:订单金额错误')
            print(json_obj['alipay_trade_pay_response']['receipt_amount'], '============',
                  cache.get('seckill_price'))
            return HttpResponse('success')
        if cache.get(f'buff:{request.userid}') == '111':  # 验证是否已经支付过一次
            print('======================该用户已经支付过一次')
            return HttpResponse('success')
        # 通过所有验证之后，修改数据库
        user = Users.objects.get(id=request.userid)
        user.vip = timezone.now() + timedelta(
            days=31 * cache.get('seckill_month')) if user.vip <= timezone.now() else user.vip + timedelta(
            days=31 * cache.get('seckill_month'))
        cache.set(f'buff:{request.userid}', '111')
        return HttpResponse('success')  # 处理完支付宝的消息后，一定要给支付宝这个回复，否则支付宝会一直发请求


def back(request):
    """
    将redis的数据转存入mysql
    暂时由管理员来执行
    """

    # 数据回收状态:有值，未回收，无值，已回收

    if r.lpop('seckill_back'):
        if (timezone.now() - cache.get('seckill_time')).seconds > cache.get('seckill_continue_time'):
            # 启动回收程序
            order_id_dict = r.hgetall('seckill_order_id')  # type:dict
            obj = SeckillBehavior.objects
            users_obj = Users.objects
            seckill_obj = SeckillMessage.objects.get(is_active=True)
            for k, v in order_id_dict.items():
                user_obj = users_obj.get(id=int(k.decode()))
                if r.hget('seckill_buff', k) != b'111':
                    __time = user_obj.vip - timezone.now()
                    if __time > timedelta(seconds=0):
                        surplus_vip_time = __time.days
                    else:
                        surplus_vip_time = 0
                else:
                    __time = user_obj.vip - timedelta(days=31 * seckill_obj.month) - timezone.now()
                    if __time > timedelta(seconds=0):
                        surplus_vip_time = __time.days
                    else:
                        surplus_vip_time = 0
                try:
                    obj.create(
                        id=v.decode(),
                        seckill_message=seckill_obj,
                        user=user_obj,
                        label=r.hget('seckill_buff', k).decode(),
                        count=r.hget('seckill_count', k).decode(),
                        surplus_vip_time=surplus_vip_time
                    )
                except Exception as e:
                    print('=================:', e)
                    continue
            r.delete('seckill_buff')
            r.delete('seckill_count')
            r.delete('seckill_order_id')
            r.delete('seckill_back')
            return JsonResponse({'code': 200})
        else:
            r.lpush('seckill_back', 1)
            return JsonResponse({'code': 10030, 'error': '秒杀未结束，或下一轮秒杀已处于激活状态'})
    else:
        return JsonResponse({'code': 10031, 'error': '没有需要回收的数据'})

