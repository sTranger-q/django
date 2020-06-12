from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index_view(request):
    # return HttpResponse('<h1>这是newsApp</h1>')
    return render(request, 'news/news_index.html')
