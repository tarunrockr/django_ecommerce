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
    minimum_price = str(request.POST.get('minimum_price'))
    maximum_price = str(request.POST.get('maximum_price'))
    #minimum_price = str(500)
    #maximum_price = str(6000)
    brand         = request.POST.get('brand')
    color         = request.POST.get('color')
    size          = request.POST.get('size')

    if brand != "":
        brand = json.loads(brand)
        brand_string1 = []
        for x in brand:
            brand_string1.append(str(x))
        brand_string = ",".join("'" + item + "'" for item in brand_string1)

    if color != "":
        color = json.loads(color)
        color_string1 = []
        for x in color:
            color_string1.append(str(x))
        color_string = ",".join("'" + item + "'" for item in color_string1)

    if size != "":
        size = json.loads(size)
        size_string = ",".join(size)

    # Making query
    cursor = connection.cursor()
    sql = "SELECT * from products_product where 1"

    # If minimum price and maximum price both exists
    if minimum_price != "" and maximum_price != "":
        sql = sql + " AND  price BETWEEN "+minimum_price+" AND "+maximum_price

    # if brand exists
    if brand_string != "":
        sql = sql + " AND brand IN("+brand_string+") "

    # if color exists
    if color_string != "":
        sql = sql + " AND color IN("+color_string+") "

    # if size exists
    if size_string != "":
        sql = sql + " AND size IN("+size_string+") "

    sql = sql + " AND status=1 "
    cursor.execute(sql)
    result = cursor.fetchall()

    print(result)

    output = ''
    if result:
        for product in result:

            output+="<div class='col-md-4 col-sm-4' >"
            output+="  <span class='thumbnail'>"
            # if product.productimage_set.all:
            #     for item in product.productimage_set.all:
            #         if item.featured:
            #             output+="< img class ='img-responsive' src='{0}'  style='height: 40% !important;' >".format(item.image.url)
            # else:
            #     output+="<img class='img-responsive' src='{% static 'images/default-image.png' %}' >"
            output += "<img class='img-responsive' src='{% static 'images/default-image.png' %}' >"
            output+="<h4>{0}</h4>".format(product[1])
            output+="<div class='ratings' >"
            output+="  <span class='glyphicon glyphicon-star'></span>"
            output+="  <span class='glyphicon glyphicon-star'></span>"
            output+="  <span class='glyphicon glyphicon-star'></span>"
            output+="  <span class='glyphicon glyphicon-star'></span>"
            output+="  <span class='glyphicon glyphicon-star-empty'></span>"
            output+="</div>"
            output+="<p>{0}</p>".format(product[2])
            output+="<p><strong> Brand: </strong> {0} </p>".format(product[9])
            output+="<p><strong> Color: </strong> {0} </p>".format(product[10])
            output+="<p><strong> Size: </strong> {0} </p>".format(product[11])
            output+="<hr class='line' >"

            output+="<div class='row'>"
            output+="  <div class='col-md-6 col-sm-6'>"
            output+="    <p class='price'>{0}</p>".format(product[3])
            output+="  </div>"
            output+="  <div class='col-md-6 col-sm-6'>"
            output+="      <a href ='{{ product.get_absolute_url }}' target='_blank' > <button class ='btn btn-info right'> View Detail </button> </a>"
            output+="  </div>"
            output+="</div>"

            output+="<div class='row'>"
            output+="  <div class='col-md-6 col-sm-6'>"
            output+="      <a class='btn btn-primary left'> Buy Now </a>"
            output+="  </div>"
            output+="  <div class='col-md-6 col-sm-6'>"
            output+="      <a href='{% url 'carts.update_cart' product.id %}' class='btn btn-primary right'> Add to Cart </a>"
            output+="  </div>"
            output+="</div>"
            output+="</span>"
            output+="</div>"

    else:
        output ='<h1> No result found.</h1>'

    data = [{'data':output}]
    return JsonResponse(data, safe=False)


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








