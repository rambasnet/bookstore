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

def deals(request):
    context = {
        'nbar': 'deals',
        'pageTitle': 'deals',
        'panelTitle': 'Deals',
        'panelBody': '<strong>Sorry! There are no deals at this time!</strong>'
    }
    return render(request, 'books/static.html', context)

def contact(request):
    context = {
        'nbar': 'contact',
        'pageTitle': 'Contact',
        'panelTitle': 'Contact',
        'panelBody': """
            <!-- List group -->
            <ul class="list-group">
            <li class="list-group-item"><strong>Corporate Office: </strong><br />
                <address>111 University Blvd<br>
                        Grand Junction, CO 81501 <br>
                        &phone;: (970) 123-4567<br>
                        <span class="glyphicon glyphicon-envelope"></span>: help@amazing.com<br>
            </li>
            <li class="list-group-item"><strong>Denver Office: </strong><br />
                <address>123 Amazing Street</br>
                        Denver, CO 81111 <br>
                        &phone;: (970) 123-1234<br>
                        <span class="glyphicon glyphicon-envelope"></span>: denver@amazing.com<br>
            </li>
            <li class="list-group-item">Porta ac consectetur ac</li>
            <li class="list-group-item">Vestibulum at eros</li>
            </ul>
        """,
    }
    return render(request, 'books/static.html', context)