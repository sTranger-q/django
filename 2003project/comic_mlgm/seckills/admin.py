from django.contrib import admin
from django.core.cache import cache
from .models import *
from .views import *
# Register your models here.


class MyModel(admin.ModelAdmin):
    """
    继承admin.ModelAdmin
    重写save_model
    """
    def save_model(self, request, obj, form, change):
        super().save_model(request,obj,form,change)
        # 下面写想要添加的逻辑，先看一下这几个参数都是什么：
        """
        print('==========================')
        print('request:',request)
        print('obj:',obj)
        print('form:',form)
        print('change:',change)
        print('=============================')
        
        ==========================
            request: <WSGIRequest: POST '/admin/seckills/seckillmessage/add/'>   这是请求对象
            obj: SeckillMessage object (1)      这是新创建的数据对象
            form: 整个页面的HTML文本
            change: False           新创建一条数据时为False，更新一条已有数据时为True
        =============================
        """
        crontab(obj.price,obj.begin_time,obj.continue_time,obj.count,obj.month)

@admin.register(SeckillMessage)
class SeckillMessageManager(MyModel):
    list_display = ['month','count','price','begin_time','continue_time','sell_out_time','surplus_count','is_active','update_time']
    list_display_links = ['begin_time']
    list_per_page = 20