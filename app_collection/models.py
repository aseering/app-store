from django.db import models
from utils.enum import Enum
from django.contrib.auth.models import User

# Create your models here.

class App(models.Model):
    statuses = Enum(PENDING="Pending",
                    ACCEPTED="Accepted")

    submitter = models.ForeignKey(User)

    submission_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    app = models.FileField(upload_to='apps')
    status = models.CharField(max_length=8,
                              choices=statuses,
                              default=statuses.PENDING)


