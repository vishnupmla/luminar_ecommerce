from django.db import models
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30)
    desc = models.TextField()
    image = models.ImageField(upload_to='category')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:products', args=[self.pk])

class Product(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    image = models.ImageField(upload_to='products')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='product')

    def __str__(self):
        return self.name