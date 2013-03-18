from django.conf.urls import patterns, include, url
from app_collection.views import list_apps, show_app

urlpatterns = patterns('',
    url(r'^', list_apps),
    url(r'^(?P<app_name>\w+)/', show_app),
)
