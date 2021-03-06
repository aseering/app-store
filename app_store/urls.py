from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
import app_store_home.urls
import app_collection.urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app_store.views.home', name='home'),
    # url(r'^app_store/', include('app_store.foo.urls')),
    url(r'^', include(app_store_home.urls)),

    url(r'^apps/', include(app_collection.urls)),

    url(r'^accounts/', include('userena.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
