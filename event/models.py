from django.db import models
from script.models import *
# Create your models here.

class Message(models.Model):
    group_id = models.CharField(max_length=30)
    registrant_id = models.CharField(max_length=30)
    group_script = models.ForeignKey(Command)
    add_time = models.DateTimeField()


class Notice(models.Model):
    private_id = models.CharField(max_length=30)
    registrant_id = models.CharField(max_length=30)
    private_script = models.ForeignKey(Command)
    add_time = models.DateTimeField()


class Request(models.Model):
    discuss_id = models.CharField(max_length=30)
    registrant_id = models.CharField(max_length=30)
    discuss_script = models.ForeignKey(Command)
    add_time = models.DateTimeField()

class Meta_event(models.Model):
    discuss_id = models.CharField(max_length=30)
    registrant_id = models.CharField(max_length=30)
    discuss_script = models.ForeignKey(Command)
    add_time = models.DateTimeField()

