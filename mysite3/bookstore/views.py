from django.shortcuts import render
from .models import *


# Create your views here.
def all_book(request):
    books = Book.objects.all()
    lis = []
    for book in books:
        lis.append(
            [book.id, book.title, book.pub, book.price, book.market_price,
             '更新 删除'])
        lis.append('换行')
    lis.pop()
    return render(request, 'bookstore/all_books.html', {'books': lis})
