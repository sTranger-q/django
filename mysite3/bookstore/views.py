from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.
def all_book(request):
    books = Book.objects.all()
    lis = []
    for book in books:
        lis.append(
            [book.id, book.title, book.pub, book.price, book.market_price])
        lis.append('换行')
    lis.pop()
    return render(request, 'bookstore/all_books.html', {'books': lis})


def update_book(request, bid):
    try:
        book = Book.objects.get(id=bid)
    except Exception as e:
        print('--update book error--')
        return HttpResponse('---book id error---')
    if request.method == 'GET':
        return render(request, 'bookstore/update_book.html', locals())
    elif request.method == 'POST':
        try:
            book.market_price = request.POST['marketPrice']
            book.save()
        except Exception as e:
            return HttpResponse('---book id error---')
        return HttpResponseRedirect('/bookstore/all_book')
