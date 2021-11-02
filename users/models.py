from os import truncate
from django.db import models

class User(models.Model):
	user 		 = models.CharField(max_length=45)
	email	 	 = models.CharField(max_length=200, unique=True)
	password 	 = models.CharField(max_length=200)
	phone_number = models.CharField(max_length=20)

	class Meta:
	   db_table = 'users'
