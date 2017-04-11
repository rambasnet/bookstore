from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.
def index(request):
    context = {'nbar': 'home', 
                'heading': 'Amazing Textbook Store',
                'mission': 'home of amazingly cheap college textbooks',
                'deals': [('black friday deal', 'https://placehold.it/150x80?text=IMAGE', 'Buy 50 mobiles and get a gift card'),
                ('christmas deal', 'https://placehold.it/150x80?text=IMAGE', 'Buy 1 mobile and get 1 free')]
            }
    return render(request, 'books/index.html', context)

def books(request):
    context = {
                'nbar': 'books',
                'products': [('image url', 'https://placehold.it/150x80?text=IMAGE', 'product name', 'description'),
                ('christmas deal', 'https://placehold.it/150x80?text=IMAGE', 'product 1 name', 'descrtiption 1')]
            }
    return render(request, 'books/books.html', context)