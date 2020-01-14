from django.shortcuts import render
from django.http import HttpResponse
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



