from django.db import models


# Create your models here.
class tbl_district(models.Model):
    districtid = models.AutoField(primary_key=True)
    districtname = models.CharField(max_length=25)


class tbl_location(models.Model):
    locationid = models.AutoField(primary_key=True)
    locationname = models.CharField(max_length=25)
    districtid = models.ForeignKey(tbl_district, on_delete=models.CASCADE)


class tbl_category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    categoryname = models.CharField(max_length=50)
    image = models.ImageField()


class tbl_subcategory(models.Model):
    subcategoryid = models.AutoField(primary_key=True)
    subcategoryname = models.CharField(max_length=25)
    image = models.ImageField()
    categoryid = models.ForeignKey(tbl_category, on_delete=models.CASCADE)


class tbl_product(models.Model):
    productid = models.AutoField(primary_key=True)
    productname = models.CharField(max_length=25)
    description = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=True)
    quantity = models.BigIntegerField(null=True)
    image = models.ImageField()
    subcategoryid = models.ForeignKey(tbl_subcategory, on_delete=models.CASCADE)
