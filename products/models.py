from django.db import models

# Create your models here.

class Product(models.Model):
    title       = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    price       = models.DecimalField(decimal_places=2, max_digits=10, default=30)
    slug        = models.SlugField()
    created_at  = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at  = models.DateTimeField(auto_now_add=False, auto_now=True)
    status     = models.BooleanField(default=True)

    def __str__(self):
        return self.title
