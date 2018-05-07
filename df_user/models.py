# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class UserInfo(models.Model):
    uname = models.CharField(max_length=10)
    upwd = models.CharField(max_length = 40)
    uemail = models.CharField(max_length = 30)
    ushou = models.CharField(max_length = 10, default='')
    uaddress = models.CharField(max_length=100, default='')
    uyoubian = models.CharField(max_length = 6, default='')
    uphone = models.CharField(max_length = 13, default='')
    # 对于default & blank 是python 层面的，不需要歉意到数据库

