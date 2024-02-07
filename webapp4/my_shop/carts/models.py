from django.db import models
from .models import Product
from .models import Customer
# Create your models here.
class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, models.DO_NOTHING, db_column='customer')
    product = models.ForeignKey(
        Product, models.DO_NOTHING, db_column='product')
    price = models.FloatField()
    quantity = models.IntegerField()

    class Meta:
        db_table = 'Carts'

    def __str__(self) -> str:
        return "Cart ID: " + str(self.id) + " Product ID: " + str(self.product.id) + " : " + str(self.quantity)