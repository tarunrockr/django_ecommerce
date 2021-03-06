from django.db import models

# Create your models here.

class Product(models.Model):
    title       = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    price       = models.DecimalField(decimal_places=2, max_digits=10, default=30)
    sale_price  = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    slug        = models.SlugField()
    created_at  = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at  = models.DateTimeField(auto_now_add=False, auto_now=True)
    status     = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)

    def get_price(self):
        return self.price


class ProductImage(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    image      = models.ImageField(upload_to='products/images/')
    featured   = models.BooleanField(default=False)
    thumbnail  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title