from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', views.login),
    url(r'^register/$', views.register),
    url(r'^create_user/$', views.create_user),
    url(r'^login_check/$', views.login_check),
    url(r'^logout/$', views.logout),
]