from django.conf.urls import url
from . import views
from models import User, Book, Author, Review

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^authenticate$', views.authenticate, name='login'),
    url(r'^books$', views.home, name='home'),
    url(r'^add$', views.add, name='add'),
    url(r'^create$', views.create, name='create'),
    url(r'^books/(?P<id>\d+)$', views.read_book, name='book'),
    url(r'^users/(?P<id>\d+)$', views.read_user, name='user'),
    url(r'^destroy/(?P<id>\d+)$', views.destroy_review, name='destroy'),
    url(r'^logout$', views.logout, name='logout')
]