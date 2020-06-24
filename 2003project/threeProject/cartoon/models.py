from django.db import models

# Create your models here.

status=('连载中','完结','新番')

class Catalog(models.Model):
    '''
    漫画标签
    '''
    create_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    name = models.CharField(max_length=10, verbose_name='漫画标签')
    clicked_num=models.IntegerField(max_length=1000,verbose_name='该类别标签的点击量')
    class Meta:
        db_table = 'PTPT_Comic_CATALOG'
        verbose_name = '漫画标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class SPU(models.Model):
    '''
    SPU 漫画表
    '''
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    name = models.CharField(max_length=50, verbose_name='名称')
    clicks = models.IntegerField(default=0, verbose_name='点击量')
    comments = models.IntegerField(default=0, verbose_name='评价数量')
    author=models.CharField(max_length=100,verbose_name='作者')
    intro=models.CharField(max_length=3000,verbose_name='作品简介')
          #这个字段我想不起来那个简介应该用那个ORM了

    catalog_id = models.ForeignKey(Catalog, on_delete=models.PROTECT, related_name='catalog_comic',
                                verbose_name='漫画类别')
    is_continued = models.BooleanField(default=True, verbose_name='是否连载')

    '''
    这个属性想做成就三个可选的值, 连载 完结 新番
    '''
    cover_path=models.CharField(max_length=300,verbose_name='封面图片存储地址')
    '''
    这地方要斟酌下,这个封面图片的问题,具体可以参考dadashop
    '''


    class Meta:
        db_table = 'PTPT_Comic_SPU'
        verbose_name = 'SPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class Most_clicked(models.Model):
    '''
    最高点击量,这里需要个遍历最高点击量的算法,存在这里面,感觉每周存一次就好，待商榷
    '''
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    SPU_ID = models.ForeignKey(SPU, on_delete=models.CASCADE, verbose_name='最热漫画')

    class Meta:
        db_table = 'PTPT_Comic_CATALOG'
        verbose_name = '漫画标签'
        verbose_name_plural = verbose_name



class SKU(models.Model):
    """
    SKU 漫画
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    name = models.CharField(max_length=50, verbose_name='SKU名称')
        #这个SKU,想了下好像起名没鸟用,跟SPU重了,别的暂时没想到这地方需不需要给那么这个字段
    caption = models.CharField(max_length=100, verbose_name='副标题')
    SPU_ID = models.ForeignKey(SPU, on_delete=models.CASCADE, verbose_name='漫画')
    Chapters_num=models.IntegerField(max_length=1000,verbose_name='一共多少话')
    Chapters_path=models.CharField(max_length=300,verbose_name='漫画地址')

    class Meta:
        db_table = 'PTPT_Comic_SKU'
        verbose_name = 'SKU表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)

class Chapter(models.Model):
    '''
    话
    '''
    name = models.CharField(max_length=50, verbose_name='话名称')
    SKU_ID = models.ForeignKey(SKU, on_delete=models.CASCADE, verbose_name='话')
    Pic_path=models.CharField(max_length=300,verbose_name='话位置')

    class Meta:
        db_table = 'PTPT_Comic_Chapter'
        verbose_name = 'Chapter表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)

