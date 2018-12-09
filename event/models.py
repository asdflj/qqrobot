from django.db import models
from script.models import *
# Create your models here.

class Message(models.Model):
    register_id = models.CharField(max_length=30)
    script = models.ForeignKey(PythonScript)
    add_time = models.DateTimeField(auto_now=True)
    error_num = models.IntegerField(default=0)
    is_ban = models.BooleanField(default=False)


class Notice(models.Model):
    register_id = models.CharField(max_length=30)
    script = models.ForeignKey(PythonScript)
    add_time = models.DateTimeField(auto_now=True)
    error_num = models.IntegerField(default=0)
    is_ban = models.BooleanField(default=False)

class Request(models.Model):
    register_id = models.CharField(max_length=30)
    script = models.ForeignKey(PythonScript)
    add_time = models.DateTimeField(auto_now=True)
    error_num = models.IntegerField(default=0)
    is_ban = models.BooleanField(default=False)

class Meta_event(models.Model):
    register_id = models.CharField(max_length=30)
    script = models.ForeignKey(PythonScript)
    add_time = models.DateTimeField(auto_now=True)
    error_num = models.IntegerField(default=0)
    is_ban = models.BooleanField(default=False)

