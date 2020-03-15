from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Product, ProductImage
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
import  json

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

    cursor = connection.cursor()

    sql="SELECT DISTINCT brand FROM products_product ORDER BY brand ASC"
    cursor.execute(sql)
    brands = cursor.fetchall()


    sql = "SELECT DISTINCT color FROM products_product ORDER BY color ASC"
    cursor.execute(sql)
    colors = cursor.fetchall()

    sql = "SELECT DISTINCT size FROM products_product ORDER BY size ASC"
    cursor.execute(sql)
    sizes = cursor.fetchall()

    product_list =  Product.objects.all()
    template     = 'products/index.html'
    context      = {'products': product_list, 'brands': brands, 'colors': colors, 'sizes':sizes}
    return render(request, template, context)

def  product_list_ajax(request):
    brand = request.POST.get('brand')
    # data = json.loads(brand)
    print(type(brand))

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

def product_search_autocomplete(request):

    query_data =request.POST.get('query')
    print(query_data)
    # Executing raw query
    cursor=connection.cursor()
    sql="SELECT title FROM products_product WHERE title LIKE '%"+query_data+"%'"
    cursor.execute(sql)
    result =  cursor.fetchall()
    output="<ul class='list-unstyled custom_style search_ul'>"
    if(result):
        for row in result:
            output+="<li class='result_li search_li' >{0}</li>".format(row[0])
    else:
        output+="<li class='search_li' >Result not found</li>"

    output+="</ul>"

    data =[{'data':output}]
    return JsonResponse(data, safe=False)

def product_search(request):
    try:
        search_data=request.GET.get('search')
    except:
        search_data=None

    # print(search_data)
    if(search_data):
        product_list = Product.objects.filter(title__icontains=search_data)
        context = {'products': product_list,'search_data': True}
    else:
        product_list = Product.objects.all()
        context={'products': product_list}
    template = 'products/product_search.html'
    return render(request, template, context)








