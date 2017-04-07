from django.conf.urls import url
from .views import index, books

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'books/$', books, name='books')
]