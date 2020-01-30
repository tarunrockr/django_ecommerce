from django.db import models
from products.models import Product
# Create your models here.

class Cart(models.Model):
    products   = models.ManyToManyField(Product, blank=True)
    total      = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    status     = models.BooleanField(default=True)

    def __str__(self):
        return  "Cart Row ID: %s"%(self.id)

