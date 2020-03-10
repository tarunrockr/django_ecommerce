from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse, Http404, JsonResponse

# Create your views here.
from .models import Cart, CartItem
from  products.models import Product

def show_cart(request):

    try:
        cart_id = request.session['cart_id']
    except:
        cart_id = None

    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        context = {'cart': cart}
    else:
        empty_message = "Your cart is empty. Continue Shopping."
        context = {'empty':True, 'empty_message': empty_message }

    template = 'carts/index.html';
    return render(request, template, context)

def update_cart(request, id):

    # Fetch product from database that is going to be add in cart
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        pass
    except:
        pass

    # Checking if cart_id is available in session or not, if it is available store it in cart_id
    try:
        cart_id = request.session['cart_id']
    except:
        # If cart_id is not available in the cart then create new row in cart table and store its id in session
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        cart_id = new_cart.id

    # Getting the cart on behalf of cart_id in session
    cart = Cart.objects.get(id=cart_id)

    # Checking if that product exists in CartItem table with that cart_id or not
    if CartItem.objects.filter(cart_id=cart_id, product_id=id).exists()==True:
        # Updating the quantity of the product for that specific cart_id
        try:
            cart_item_row = CartItem.objects.get(cart_id=cart_id, product_id=id)
            cart_item_row.quantity = cart_item_row.quantity + 1
            cart_item_row.line_total = cart_item_row.quantity * float(product.price)
            cart_item_row.save()
        except:CartItem.DoesNotExist
        print('CartItem does not exists')
    else:
        # Adding the product in CartItem for first time for the cart_id
        cart_item_obj=CartItem.objects.create(quantity=1, line_total=product.price, cart_id=cart_id, product_id=id)


    new_total=0.00
    for item in cart.cartitem_set.all():
        new_total  += float(item.line_total)
    request.session['cart_item_count'] = cart.cartitem_set.count()
    cart.total = new_total
    cart.save()

    return HttpResponseRedirect(reverse('carts.show_cart'))

def remove_cart_product(request, id):

    # Getting the cart_id from the sesison
    cart_id = request.session['cart_id']

    # Getting the cart on behalf of cart_id in session
    cart = Cart.objects.get(id=cart_id)

    # Checking if product is present for the car or not
    if CartItem.objects.filter(cart_id= cart_id, product_id=id).exists()==True:
        instance=CartItem.objects.get(cart_id= cart_id, product_id=id)
        instance.delete()

    # Updating the cart
    new_total = 0.00
    for item in cart.cartitem_set.all():
        new_total += float(item.line_total)
    request.session['cart_item_count'] = cart.cartitem_set.count()
    cart.total = new_total
    cart.save()

    return HttpResponseRedirect(reverse('carts.show_cart'))

def decrease_cart_item(request):

    product_id = request.POST.get('product_id')

    # Getting the cart_id from the session
    cart_id = request.session['cart_id']

    # Getting the cart on behalf of cart_id in session
    cart = Cart.objects.get(id=cart_id)

    # Checking if product is present in cart or not
    if CartItem.objects.filter(cart_id=cart_id, product_id=product_id).exists() == True:
        instance = CartItem.objects.get( cart_id=cart_id, product_id=product_id)
        if(instance.quantity > 1):
            # Get product data
            product = Product.objects.get(pk=product_id)
            instance.quantity   = instance.quantity - 1
            instance.line_total = instance.quantity *float(product.price)
            instance.save()
        else:
            instance.delete()

    # Updating the cart
    new_total = 0.00
    for item in cart.cartitem_set.all():
        new_total += float(item.line_total)
    request.session['cart_item_count'] = cart.cartitem_set.count()
    cart.total = new_total
    cart.save()

    data = [{'data': 'ok'}]
    return JsonResponse(data, safe=False)

def increase_cart_item(request):
    product_id = request.POST.get('product_id')

    # Getting the cart_id from the session
    cart_id = request.session['cart_id']

    # Getting the cart on behalf of cart_id in session
    cart = Cart.objects.get(id=cart_id)

    # Checking if product is present in cart or not
    if CartItem.objects.filter(cart_id=cart_id, product_id=product_id).exists() == True:
        instance = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
        # Get product data
        product = Product.objects.get(pk=product_id)
        instance.quantity = instance.quantity + 1
        instance.line_total = instance.quantity * float(product.price)
        instance.save()


    # Updating the cart
    new_total = 0.00
    for item in cart.cartitem_set.all():
        new_total += float(item.line_total)
    request.session['cart_item_count'] = cart.cartitem_set.count()
    cart.total = new_total
    cart.save()

    data = [{'data': 'ok'}]
    return JsonResponse(data, safe=False)



