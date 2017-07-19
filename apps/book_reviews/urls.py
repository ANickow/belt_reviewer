from django.conf.urls import url
from . import views
from models import User, Book, Author, Review

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^authenticate$', views.authenticate),
    url(r'^books$', views.home),
    url(r'^add$', views.add),
    url(r'^create$', views.create),
    url(r'^books/(?P<id>\d+)$', views.read_book),
    url(r'^users/(?P<id>\d+)$', views.read_user),
    url(r'^destroy/(?P<id>\d+)$', views.destroy_review),
    url(r'^logout$', views.logout)
]