from django.db import models
from user.models import *
# Create your models here.



class PythonScript(models.Model):
    name = models.TextField(verbose_name='脚本名字',unique=True)
    path = models.TextField(verbose_name='脚本路径')
    creator = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now=True)

class Command(models.Model):
    external_name = models.TextField(unique=True)
    inside_name = models.ForeignKey(PythonScript)
    last_bind_user_id = models.CharField(max_length=20)
    last_bind_time = models.DateTimeField(auto_now=True)
    is_ban = models.BooleanField(default=False)

class Help(models.Model):
    command = models.TextField(unique=True)
    explain = models.TextField()
    create_time = models.DateTimeField(auto_now=True)