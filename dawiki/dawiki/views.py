from django.shortcuts import render


def index_view(request):
    user = request.session.get('username')

    return render(request, 'index.html', locals())
