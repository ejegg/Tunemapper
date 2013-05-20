from django.conf.urls import patterns, url

from tracks import views

urlpatterns = patterns('',
    url(r'^(?P<artist>[^/]+)/(?P<title>[^/]+)$', views.lookup, name='lookup')
) 
