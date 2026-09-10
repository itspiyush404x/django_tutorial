from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=250, unique=True)
    price = models.FloatField()
    description = models.CharField(max_length=3000)
    category = models.CharField(max_length=250)
    image = models.CharField()

    def product_dict(self):
        return {"id": self.id, "title": self.title, "price": self.price, "description": self.description, "category": self.category, "image": self.image}


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)



