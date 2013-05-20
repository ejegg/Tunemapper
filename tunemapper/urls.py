from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^trips/', include('trips.urls')),
    url(r'^/$', include('trips.urls')),
    url(r'^$', include('trips.urls')),
    url(r'^tracks/', include('tracks.urls')),
    # Examples:
    # url(r'^$', 'tunemapper.views.home', name='home'),
    # url(r'^tunemapper/', include('tunemapper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
