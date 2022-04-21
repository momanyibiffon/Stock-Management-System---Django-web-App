from django.db import models
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name


class BottleVolume(models.Model):
    bottle_capacity = models.CharField(max_length=50, unique=True)

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bottle_capacity


class Product(models.Model):
    product_name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    bottle_capacity = models.ForeignKey(BottleVolume, on_delete=models.SET_NULL, null=True)
    price_per_crate = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=10)
    email_address = models.EmailField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.supplier_name


class Client(models.Model):
    client_name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=10, unique=True)
    email_address = models.EmailField(max_length=100, blank=True, unique=True)
    location = models.CharField(max_length=50, blank=True)

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    reg_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name


class SaleProduct(models.Model):
    product_name = models.CharField(max_length=100, blank=True)
    sold_bottle_capacity = models.ForeignKey(BottleVolume, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    price_per_crate = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    sale_total_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ReceiveProduct(models.Model):
    product_name = models.CharField(max_length=100, blank=True)
    received_bottle_capacity = models.ForeignKey(BottleVolume, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    r_price_per_crate = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    total_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
