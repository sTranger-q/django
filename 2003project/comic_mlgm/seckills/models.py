from django.db import models

# Create your models here.
from django.utils import timezone
from user.models import Users

class SeckillMessage(models.Model):
    month = models.IntegerField('VIP月数')
    count = models.IntegerField('秒杀数量')
    price = models.DecimalField('价格',max_digits=6,decimal_places=2)
    begin_time = models.DateTimeField('开启时间',default=timezone.now)
    continue_time = models.IntegerField('持续时间(s)')
    sell_out_time = models.IntegerField('售罄时间',default=99999)
    surplus_count = models.IntegerField('剩余数量',default=-1)
    is_active = models.BooleanField('激活状态',default=True)
    update_time = models.DateTimeField('修改时间',auto_now=True)

    class Meta:
        db_table = 'seckill_message'

class SeckillBehavior(models.Model):
    id = models.CharField('时间戳',max_length=50,primary_key=True)
    seckill_message = models.ForeignKey(SeckillMessage,on_delete=models.PROTECT)
    user = models.ForeignKey(Users,on_delete=models.PROTECT)
    label = models.CharField('标签',max_length=3)
    count = models.IntegerField('尝试抢购次数')
    surplus_vip_time = models.IntegerField('参与秒杀时，用户剩余VIP天数')

    class Meta:
        db_table = 'seckill_behavior'