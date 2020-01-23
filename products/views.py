from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Product, ProductImage
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# def index(request):
#     # if request.user.is_authenticated():
#     #     username = 'Uri Boyka'
#     #     context={'username': username}
#     # else:
#     #     context={'username': 'unknown'}
#
#     context = {'username': 'unknown'}
#
#     template = 'products/index.html'
#     return render(request, template, context )


def product_list(request):

    product_list =  Product.objects.all()
    template     = 'products/index.html'
    context      = {'products': product_list}
    return render(request, template, context)

def product_detail(request, id):

    # try:

        # Fetching specific product detail
        product_data = Product.objects.raw("SELECT * FROM products_product WHERE id=%s", [id])[0]
        # product_data = Product.objects.get(id=id)

        # Fetching all the images related to this product

        #product_images = ProductImage.objects.filter(product=product_data.id)
        product_images = ProductImage.objects.raw("SELECT * FROM products_productimage WHERE product_id = %s", [product_data.id])
        # print(product_images)


        template = 'products/productDetail.html'
        context={'product_data': product_data, 'product_images': product_images}
        return render(request, template, context)
    # except:
    #     raise Http404






