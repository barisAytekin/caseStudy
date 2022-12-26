from django.db import models

# Create your models here.

class User (models.Model):
    id = models.AutoField(primary_key = True) #her yeni kayit geldiginde auto increment et
    name = models.CharField(max_length=100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
