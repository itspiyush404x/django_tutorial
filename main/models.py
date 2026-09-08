from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=250)
    price = models.FloatField()
    description = models.CharField(max_length=3000)
    category = models.CharField(max_length=250)
    image = models.CharField()

