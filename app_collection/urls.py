from django.conf.urls.defaults import patterns, include, url
from app_collection.views import list_apps, list_apps_json, show_app, show_app_json, my_apps, submit_app, submit_instance

urlpatterns = patterns('',
    url(r'^$', list_apps, {}, "list_apps"),
    url(r'^list.json$', list_apps_json),
    url(r'^submit/', submit_app, {}, "apps/submit"),
    url(r'^submit_instance/', submit_instance, {}, "apps/submit_instance"),
    url(r'^my', my_apps, {}, "apps/my"),
    url(r'^(?P<app_name>[\w-]+)/$', show_app, {}, "apps/show_app"),
    url(r'^(?P<app_name>[\w-]+)/app.json', show_app_json),
)
