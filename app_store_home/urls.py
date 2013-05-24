from django.conf.urls.defaults import patterns, url
from app_store_home.views import HomePageView, AboutView, DownloadView

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view()),
    url(r'^about.html$', AboutView.as_view(), {}, "about"),
    url(r'^download_verticapp.html$', DownloadView.as_view(), {}, "verticapp_download"),

)
