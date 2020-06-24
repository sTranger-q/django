from django.http import JsonResponse
from django.shortcuts import render
from .templates.music.MusicSp import music_html
from .models import Music
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.

def music_view(request):
    if request.method == 'GET':
        data = Music.objects.all()[:50]
        paginator = Paginator(data, 10)
        try:
            page = request.GET.get('page', '1')
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'music/music.html', {'contacts': contacts, 'paginators': paginator})

