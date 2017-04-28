# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	phone = models.CharField(max_length=20)
	birthday = models.DateField()
	role = models.IntegerField(default=0)
	ROLE = {'USER':0, 'VIP':1, 'MANAGER':2}
	is_license = models.BooleanField(default=False)
	auth_email = models.BooleanField(default=False)
	auth_phone = models.BooleanField(default=False)

	def __unicode__(self):
		return self.first_name +self.last_name