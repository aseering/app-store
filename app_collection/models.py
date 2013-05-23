from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from app_store import settings
from utils.enum import Enum

import hashlib

# Create your models here.

def app_upload_path_name(instance, filename):
    h = hashlib.sha1(filename + str(datetime.now()) + settings.FILENAME_SALT).hexdigest()
    return "uploaded_apps/%s/%s/%s/%s" % (h[0:3], h[3:6], h[6:], filename)


class App(models.Model):
    statuses = Enum(PENDING="Pending",
                    ACCEPTED="Accepted")

    submitter = models.ForeignKey(User)

    submission_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=64, unique=True)
    shortname = models.CharField(max_length=64, unique=True)
    description = models.TextField()

    status = models.CharField(max_length=8,
                              choices=statuses,
                              default=statuses.PENDING)
    
    github_account = models.CharField(max_length=64,
                                      help_text="i.e., http://github.com/<i><b>account</b></i>/<i>project</i>")
    github_project = models.CharField(max_length=64,
                                      help_text="i.e., http://github.com/<i>account</i>/<i><b>project</b></i>")

    @property
    def github_url(self):
        return "https://github.com/%s/%s" % (github_account, github_project)
    
    @property
    def github_readme(self):
        return "https://raw.github.com/%s/%s/master/README.txt" % (github_account, github_project)

    @property
    def github_zip(self):
        return "https://github.com/%s/%s/archive/master.zip" % (github_account, github_project)

    def __unicode__(self):
        return self.name

class ApiVersion(models.Model):
    ## TODO: Should be distinct on ( ... well, everything)
    brand_version = models.CharField(max_length=32)
    sdk_version = models.CharField(max_length=64)

    def __unicode__(self):
        return self.brand_version

class AppInstance(models.Model):
    ## TODO: Should be distinct on (app, api_version)
    app = models.ForeignKey(App)
    api_version = models.ForeignKey(ApiVersion)

    setup_sql = models.TextField(help_text='Installer script will prepend "\set libfile \'/path/to/your/App.so\'"')
    remove_sql = models.TextField(help_text='Installer script will prepend "\set libfile \'/path/to/your/App.so\'"')

    so_file = models.FileField(upload_to=app_upload_path_name)
    tarball = models.FileField(upload_to=app_upload_path_name, blank=True, null=True)

    def __unicode__(self):
        return "%s: %s" % (self.app.name, self.api_version.sdk_version)
