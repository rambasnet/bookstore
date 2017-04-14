from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'books/$', views.book_list, name='books'),
    url(r'deals/', views.deals, name='deals'),
    url(r'contact/$', views.contact, name='contact'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.book_detail, 
        name='book_detail'),
]