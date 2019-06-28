from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=30)

class Stocks_Temp(models.Model):
    company = models.CharField(max_length=10)
    price = models.IntegerField()


