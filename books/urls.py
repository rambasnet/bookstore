from django.conf.urls import url
from .views import index, books, contact, deals

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'books/$', books, name='books'),
    url(r'deals/', deals, name='deals'),
    url(r'contact/$', contact, name='contact')
]