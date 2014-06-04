#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^login', 'qaz_login.views.user_login'),
)
