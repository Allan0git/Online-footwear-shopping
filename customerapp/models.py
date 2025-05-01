from django.db import models

from adminapp.models import tbl_product
from footwearapp.models import tbl_login


class tbl_cart(models.Model):
    cartid = models.AutoField(primary_key=True)
    productid = models.ForeignKey(tbl_product, on_delete=models.CASCADE)
    customer = models.ForeignKey(tbl_login, on_delete=models.CASCADE)
    quantity = models.BigIntegerField()
    billno = models.IntegerField(null=True)
    status = models.CharField(max_length=50)


class Book(models.Model):
    BookId = models.AutoField(primary_key=True)
    booking_date = models.DateField(auto_now_add=True)
    TotalAmount = models.FloatField()
    customer = models.ForeignKey(tbl_login, on_delete=models.CASCADE)
    billno = models.IntegerField(default=100)
    status = models.CharField(max_length=50)


class Payment(models.Model):
    PaymentId = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    TotalAmount = models.FloatField()
    deliveryaddress = models.CharField(max_length=100, null=True)


