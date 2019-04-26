from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^new_list/$', views.new_list),
    url(r'^create_list/$', views.create_list),
]