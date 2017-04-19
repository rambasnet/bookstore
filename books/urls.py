from django.conf.urls import url
from . import views

#app_name = 'books'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.book_list, name='books'),
    url(r'^deals/$', views.deals, name='deals'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.book_detail, 
        name='book_detail'),
    url(r'^subscribe/', views.subscribe, name='subscribe'),
    url(r'^login', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^account/', views.account, name='account'),
    url(r'^search', views.search, name='search')
]