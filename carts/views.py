from django.shortcuts import render, HttpResponseRedirect
from  django.urls import reverse

# Create your views here.
from .models import Cart
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

    try:
        # Checking if cart_id is available in session or not
        cart_id = request.session['cart_id']
    except:
        # If cart_id is not available in the cart then create new row in cart table and store its id in session
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        cart_id = new_cart.id

    cart = Cart.objects.get(id=cart_id)
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        pass
    except:
        pass
    if not product in cart.products.all():
        cart.products.add(product)
    else:
        cart.products.remove(product)

    new_total=0.00
    for item in cart.products.all():
        new_total += float(item.price)
    request.session['cart_item_count'] = cart.products.count()
    cart.total = new_total
    cart.save()

    return HttpResponseRedirect(reverse('carts.show_cart'))