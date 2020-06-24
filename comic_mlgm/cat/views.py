from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from book.models import *


# Create your views here.
def main(request):
    if request.method == 'GET':
        return render(request, 'cat/main.html')
    if request.method == 'POST':
        try:
            book_id = int(request.POST['ID'])
            chapter = int(request.POST['chapter'])
        except Exception:
            return HttpResponse('数据错误')
        try:
            book = ComicPath.objects.get(id_id=book_id)
        except Exception:
            return HttpResponse("没有这本书")
        # if chapter <= book.open_number:

        list_1 = []
        count = 1
        while True:
            try:
                picture = PictureName.objects.get(pictureID=book_id << 24 | int(chapter) << 8 | count)
            except Exception:
                if count == 1:
                    return HttpResponse('没有这个章节')
                break
            list_1.append(f'static/book/img/{book_id}/{book.open_name}/{chapter}/{picture.picture_name}.jpg')
            count += 1
        return render(request, 'cat/cat.html', {'comic': list_1})
