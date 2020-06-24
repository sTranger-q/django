from django.shortcuts import render


def test_view(request):
    return render(request, 'test_xhr.html')

def test_xhr_get(request):
    return render(request,'test_xhr_get.html')