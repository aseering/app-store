from django.contrib import admin
from app_collection.models import App, AppInstance, ApiVersion

for m in (App, AppInstance, ApiVersion):
    admin.site.register(m)
