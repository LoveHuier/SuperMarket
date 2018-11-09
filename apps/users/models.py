from datetime import datetime

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name=u'姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name=u'出生年月')
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name=u'电话')
    email = models.EmailField(null=True, blank=True, verbose_name=u'邮箱s')
    gender = models.CharField(choices=(('male', u'男'), ('female', u'女')), default='female', max_length=6,
                              verbose_name=u'性别')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name='电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
