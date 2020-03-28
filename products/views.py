from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Product, ProductImage
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
import  json
import os
from django.conf import settings

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


    skip_count    = str(request.POST.get('last_id'))

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

    total_count_sql = sql

    if skip_count != 0:
        sql = sql + " AND status=1 ORDER BY id ASC LIMIT "+skip_count+", 3  "
    else:
        sql = sql + " AND status=1 ORDER BY id ASC LIMIT 3 "


    print(sql)

    # Making an sql string to count total number of records
    count_cursor = connection.cursor()
    total_count_sql += " AND status=1"
    print(total_count_sql)
    count_cursor.execute(total_count_sql)
    total_record = count_cursor.fetchall()
    total_record_count = len(total_record)

    cursor.execute(sql)
    result = cursor.fetchall()

    output = ''
    if result:
        output += "<div class='row'>"

        for product in result:

            # Incrementing the total skip elements
            skip_count = int(skip_count)+1

            # Fetching product images -- START
            cursor1 = connection.cursor()
            product_image_sql = "SELECT * FROM products_productimage WHERE product_id="+str(product[0])
            cursor1.execute(product_image_sql)
            product_image_result = cursor1.fetchall()
            # Fetching product images -- END


            output+="<div class='col-md-4 col-sm-4' >"
            output+="  <span class='thumbnail'>"
            if product_image_result:
                for item in product_image_result:
                    if item[2]:
                        output+="<a href ='product_detail/{0}' target='_blank' > <img class='img-responsive' src='{1}'  style='height: 18% !important;' > </a>".format(product[0], os.path.join(settings.MEDIA_URL, item[1]))
            else:
                output+= "<a href ='product_detail/{0}' target='_blank'> <img class='img-responsive' src='{1}' > </a>".format(product[0], os.path.join(settings.STATIC_URL, 'images/default-image.png'))
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
            output+="      <a href ='product_detail/{0}' target='_blank' > <button class ='btn btn-info right'> View Detail </button> </a>".format(product[0])
            output+="  </div>"
            output+="</div>"

            output+="<div class='row'>"
            output+="  <div class='col-md-6 col-sm-6'>"
            output+="      <a class='btn btn-primary left'> Buy Now </a>"
            output+="  </div>"
            output+="  <div class='col-md-6 col-sm-6'>"
            output+="      <a href='carts/update_cart/{0}' class='btn btn-primary right'> Add to Cart </a>".format(product[0])
            output+="  </div>"
            output+="</div>"
            output+="</span>"
            output+="</div>"

        output+="</div>"

        # Check if more result is available with last primary key
        # cursor2 = connection.cursor()
        # sql = "Select * FROM products_product where id > {0}".format(product[0])
        # cursor2.execute(sql)
        # check_more_result = cursor2.fetchall()
        # if check_more_result:
        if skip_count < total_record_count:
            output += "<div class='row text-center'>"
            output += "<a href='javascript:void(0);' class='btn btn-lg btn-block btn-default load_more_class' last-id='{0}' >Load More</a>".format(skip_count)
            output += "</div><br>"

    else:
        if skip_count != 0:
            output = None
        else:
            output += "<div class ='alert alert-warning text-center' ><span style='font-size:25px;'><strong>No result found.</strong></span></div>"

    data = [{'data': output}]
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








