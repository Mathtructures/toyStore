from django.db import models
from shop.models import Product
# Create your models here.


class ShoppingCart(models.Model):
    totalPrice = models.IntegerField(default=0)
    products = models.ManyToManyField(Product, blank=True)

    def calTotalPrice(self):
        price = 0
        for prod in self.products.all():
            price += prod.price
        self.totalPrice = price
        return price

    def clearCart(self):
        self.totalPrice = 0
        self.products.clear()
