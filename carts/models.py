from django.db import models
from products.models import Product
# Create your models here.

class Cart(models.Model):
    total       = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    created_at  = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at  = models.DateTimeField(auto_now_add=False, auto_now=True)
    status      = models.BooleanField(default=True)

    def __str__(self):
        return  "Cart ID: %s"%(self.id)

class CartItem(models.Model):

    cart        = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity    = models.IntegerField(default=1)
    line_total  = models.DecimalField(max_digits=60, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at  = models.DateTimeField(auto_now_add=False, auto_now=True)
    status      = models.BooleanField(default=True)

    def __str__(self):
        return  self.product.title

