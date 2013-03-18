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
    app = models.FileField(upload_to=app_upload_path_name)
    status = models.CharField(max_length=8,
                              choices=statuses,
                              default=statuses.PENDING)

    def __unicode__(self):
        return "<App: %s>" % self.name
