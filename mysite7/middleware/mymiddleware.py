from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import re


class MyMiddleWare(MiddlewareMixin):
    # visit_times = {}

    def process_request(self, request):
        # ip_address = request.META['REMOTE_ADDR']
        # if not re.match(r'^/test', request.path_info):
        #     return
        # times = self.visit_times.get(ip_address, 0)
        # print('ip: %s 访问了%s次' % (ip_address, times))
        # if times >= 5:
        #     return HttpResponse('访问次数超过限制')
        # self.visit_times[ip_address] = times + 1
        return

    def process_view(self, request, callback, callback_args, callback_kwargs):
        return

    def process_response(self, request, response):
        return response

