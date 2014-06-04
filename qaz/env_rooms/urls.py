#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^envs', 'env_rooms.views.envs_home'),
    url(r'^env/(?P<env>[\w@]+)', 'env_rooms.views.env'),
    url(r'^upload/$', 'env_rooms.views.upload'),
)
