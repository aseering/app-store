from django.conf.urls import patterns, include, url
from app_collection.views import list_apps, show_app, my_apps, submit_app

urlpatterns = patterns('',
    url(r'^$', list_apps),
    url(r'^a_(?P<app_name>\w+)/', show_app),
    url(r'^submit/', submit_app, {}, "apps/submit"),
    url(r'^my/', my_apps),
)
