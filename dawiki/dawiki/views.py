from django.shortcuts import render


def index_view(request):
    username = request.session.get('username')
    if not username:
        username = request.COOKIES.get('username')

    return render(request, 'index.html', locals())
