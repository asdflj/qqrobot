from django.db import models
from script.models import *
# Create your models here.

class Message(models.Model):
    register_id = models.CharField(max_length=30,verbose_name='注册者ID')
    script = models.ForeignKey(PythonScript,verbose_name='脚本')
    add_time = models.DateTimeField(auto_now=True,verbose_name='添加时间')
    error_num = models.IntegerField(default=0,verbose_name='错误次数')
    is_ban = models.BooleanField(default=False,verbose_name='已禁用')

    def __str__(self):
        return self.script.name

    class Meta:
        verbose_name = '消息'
        verbose_name_plural=verbose_name

class Notice(models.Model):
    register_id = models.CharField(max_length=30,verbose_name='注册者ID')
    script = models.ForeignKey(PythonScript,verbose_name='脚本')
    add_time = models.DateTimeField(auto_now=True,verbose_name='添加时间')
    error_num = models.IntegerField(default=0,verbose_name='错误次数')
    is_ban = models.BooleanField(default=False,verbose_name='已禁用')

    def __str__(self):
        return self.script.name

    class Meta:
        verbose_name = '公告'
        verbose_name_plural=verbose_name


class Request(models.Model):
    register_id = models.CharField(max_length=30,verbose_name='注册者ID')
    script = models.ForeignKey(PythonScript,verbose_name='脚本')
    add_time = models.DateTimeField(auto_now=True,verbose_name='添加时间')
    error_num = models.IntegerField(default=0,verbose_name='错误次数')
    is_ban = models.BooleanField(default=False,verbose_name='已禁用')

    def __str__(self):
        return self.script.name

    class Meta:
        verbose_name = '请求'
        verbose_name_plural=verbose_name


class Meta_event(models.Model):
    register_id = models.CharField(max_length=30,verbose_name='注册者ID')
    script = models.ForeignKey(PythonScript,verbose_name='脚本')
    add_time = models.DateTimeField(auto_now=True,verbose_name='添加时间')
    error_num = models.IntegerField(default=0,verbose_name='错误次数')
    is_ban = models.BooleanField(default=False,verbose_name='已禁用')

    def __str__(self):
        return self.script.name

    class Meta:
        verbose_name = '源事件'
        verbose_name_plural=verbose_name