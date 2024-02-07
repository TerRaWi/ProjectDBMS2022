from django.db import models
from django.forms import model_to_dict

class Category(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive")
    )

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the category",
    )

    class Meta:
        # Table's name
        db_table = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name
    
# Create your models here.
class Product(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive")
    )

    name = models.CharField(max_length=256)
    image_url = models.TextField(max_length=512,default='')

    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the product",default='ACTIVE'
    )
    category = models.ForeignKey(
        Category, related_name="category", on_delete=models.CASCADE, db_column='category', blank=True, null=True)
    cost = models.FloatField(default=0)

    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    
    class Meta:
        # Table's name
        db_table = "Product"

    def __str__(self) -> str:
        return self.name

    def to_json(self):
        item = model_to_dict(self)
        item['id'] = self.id
        item['name'] = self.name
        item['image_url'] = self.image_url
        item['category'] = self.category.name
        item['quantity'] = 1
        item['total_product'] = 0
        return item
    
