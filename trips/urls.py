from django.conf.urls import patterns, url

from trips import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<trackNum>\d+)$', views.index, name='index'),
    url(r'^(?P<trackNum>\d+)/$', views.index, name='index')
)
                        