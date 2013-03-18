from django.conf.urls import patterns, include, url
import app_store_home.urls
import app_collection.urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app_store.views.home', name='home'),
    # url(r'^app_store/', include('app_store.foo.urls')),
    url(r'^$', include(app_store_home.urls)),

    url(r'^apps/', include(app_collection.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
