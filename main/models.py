from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=250)
    price = models.FloatField()
    description = models.CharField(max_length=3000)
    category = models.CharField(max_length=250)
    image = models.CharField()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)



