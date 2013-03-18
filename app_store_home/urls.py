from django.conf.urls import patterns, url
from app_store_home.views import HomePageView

urlpatterns = patterns('',
    url(r'^$', HomePageView),
)
