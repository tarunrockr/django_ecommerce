from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage

class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields =['title', 'description']
    list_display = ['__str__', 'title', 'description', 'price', 'status', 'created_at', ]
    list_filter = ['price', 'status']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',) }
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
