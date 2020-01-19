from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Product

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
        product_data = Product.objects.raw("SELECT * FROM products_product WHERE id=%s", [id])[0]
        # product_data = Product.objects.get(id=id)
        template = 'products/productDetail.html'
        context={'product_data': product_data}
        return render(request, template, context)
    # except:
    #     raise Http404






