from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
# from haystack.query import EmptySearchQuerySet
# from haystack.forms import  ModelSearchForm
from django_redis import get_redis_connection
import json
# from dadashop.settings import PIC_URL

from .models import *


# Create your views here.
class ComicIndexView(View):
    def get(self, request):
        """
        首页漫画各项展示：
        1.最大轮播图 展示 点击量前6名  SPU里面 click点击量属性取前6,播放封面图片轮播
        2.分类标签展示:  catalog
        3.本站推荐:  (就是花钱的老板的产品)  这个具体怎么体现再商量
        4.日更新:   (create_time==今天) 再取clicks点击量前5名
        5.分类标签1及其下面的5个SPU
        6.分类标签2及其下面的5个SPU
        7.分类标签3及其下面的5个SPU
        :param result:
        :return:
        """
        # 127.0.0.1:8000/cartoon
        # 0. 获取所有分类标签
        catalog_list = Catalog.objects.all()
        # 1. redis里面的东西
        index_data = {}
        # # 从redis中获取所有数据
        redis_conn = get_redis_connection('spu')  # 这地方做好接口
        redis_index = redis_conn.get('index_cache')  # 拿整个redis缓存页面
        if redis_index is None:
            print("未使用缓存")
            # 1.1 获取最大轮播图(即点击量最高作品)
            #  这部分先设定初始值,待用户使用后每周遍历一次SPU,把前6存入最高点击量表
            most_clicked = Most_clicked.objects.all()
            most_clicked_cover = SPU.objects.filter(id=most_clicked.SPU_ID)
            index_data['most_clicked'] = most_clicked_cover  # 这里想做 轮播点击量最高的6个作品的封面
            catalog_most_clicked = Catalog.objects.order_by('clicked_num')[:3]
            # 1.2  获取所有标签 并存在字典里面
            for cata in catalog_list:
                catalog_dic = {}
                catalog_dic["catalog_id"] = cata.id
                catalog_dic["catalog_name"] = cata.name
                index_data['classification_label'] = (catalog_dic)
            # 1.3  获取最热分类标签1的前5最热 存在字典里面
            label1 = SPU.objects.filter(catalog_id=catalog_most_clicked[0].objects.value('id')).order_by(
                'clicks').value_list('name', 'cover_path')[:5]
            index_data['label1'] = label1
            # 1.4  获取最热分类标签2的前5最热 存在字典里面
            label2 = SPU.objects.filter(catalog_id=catalog_most_clicked[1].objects.value('id')).order_by(
                'clicks').value_list('name', 'cover_path')[:5]
            index_data['label2'] = label2
            # 1.3  获取最热分类标签3的前5最热 存在字典里面
            label3 = SPU.objects.filter(catalog_id=catalog_most_clicked[2].objects.value('id')).order_by(
                'clicks').value_list('name', 'cover_path')[:5]
            index_data['label3'] = label3
            redis_conn.set("index_cache", json.dumps(index_data))
        else:
            print("使用缓存")
            index_data = json.loads(redis_index)
        result = {"code": 200, "data": index_data, "base_url": PIC_URL}
        # classification_list=Classification.object.all()
        #
        return JsonResponse(result)


class ComicSPU(View):
    def get(self, request, SPU_id):
        """
        1.详情页SPU 获取作品名字,作者,封面图片,简介点击量
        2.获取所有章节 章节名字 前100行数据?? 我们漫画图片这地方看情况,
        如果是整话都是一张图片的话,这方就弄个这张图片大概第一页,用f.read()就好
        3.评论区  --->待讨论
        :param request:
        :param SPU_id:
        :return: result
        """
        # 1. redis里面的东西
        index_data = {}
        # # 从redis中获取所有数据
        redis_conn = get_redis_connection('spu')  # 这地方做好接口
        redis_index = redis_conn.get('index_cache')  # 拿整个redis缓存页面
        if redis_index is None:
            print("未使用缓存")
            # 1.1 获取SPU数据,该漫画基本信息
            name = SPU.objects.value('name')
            clicks = SPU.objects.value('clicks')
            author = SPU.objects.value('author')
            intro = SPU.objects.value('intro')
            cover_path = SPU.objects.value('cover_path')
            spu_dic = {}
            spu_dic['name'] = name
            spu_dic['clicks'] = clicks
            spu_dic['author'] = author
            spu_dic['intro'] = intro
            spu_dic['cover_path'] = cover_path
            # 这地方感觉自己写的蠢到不能再蠢,希望你们改进下
            sku = SKU.objects.filter(SPU_ID=SPU_id)
            page = sku.Chapters_num // 24
            # 这地方分页 你们帮我做下了
            chapter = Chapter.objects.all()
            for i in range(24):
                pass

                # 分页这地方 就可以用 chapter.name,一页24话
            redis_conn.set("index_cache", json.dumps(index_data))
            # 分页导致这个给redis 数据的时候不好弄，斟酌下
        else:
            print("使用缓存")
            index_data = json.loads(redis_index)
        result = {"code": 200, "data": index_data}
        # classification_list=Classification.object.all()
        #
        return JsonResponse(result)


class ComicDetailView(View):
    def get(self, request, sku_id):
        """
        获取chapter名字,和图片路径

        :param request:
        :param sku_id: sku的id
        :return:
        """

        # 获取sku实例,该话的名字,该话的图片存储地址
        chapter = Chapter.objects.all()
        dic_chapter = {}
        dic_chapter['name'] = chapter.name
        dic_chapter['Pic_path'] = chapter.Pic_path
        result = {"code": 200, "data": dic_chapter}
        return JsonResponse(result)
