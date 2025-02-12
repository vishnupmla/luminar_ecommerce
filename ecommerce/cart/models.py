from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='pdct')
    quantity = models.IntegerField()
    data_added = models.DateTimeField(auto_now_add=True)

    def subTotal(self):
        return self.product.price * self.quantity


    def __str__(self):
        return self.product.name

class OrderDetails(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    no_of_items = models.IntegerField()
    address = models.TextField()
    phone = models.BigIntegerField()
    pin = models.IntegerField()
    order_id = models.CharField(max_length=30)
    payment_status = models.CharField(max_length=30,default='pending')
    delivery_status = models.CharField(max_length=30,default='pending')
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

class Payment(models.Model):
    name = models.CharField(max_length=30)
    amount = models.IntegerField()
    order_id = models.CharField(max_length=30)
    razorpay_payment_id = models.CharField(max_length=30,blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.order_id

