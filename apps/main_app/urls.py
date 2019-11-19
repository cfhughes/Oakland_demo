from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register', views.register),
    url(r'^logout', views.logout),
    url(r'^home', views.home),
    url(r'^profile', views.profile),
    url(r'^wow', views.wow),
]
