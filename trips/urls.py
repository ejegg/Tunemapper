from django.conf.urls import patterns, url

from trips import views

urlpatterns = patterns('',
    url(r'^requests.php$', views.upload),
    url(r'^$', views.index),
    url(r'^(?P<trackNum>\d+)$', views.index),
    url(r'^(?P<trackNum>\d+)/$', views.index)
)