from django.urls import path
from .import views

urlpatterns=[
    path('', views.show_cart, name='carts.show_cart'),
    path('update_cart/<int:id>/', views.update_cart, name='carts.update_cart'),
    path('remove_cart_product/<int:id>/', views.remove_cart_product, name='carts.remove_cart_product'),
    path('decrease_cart_item', views.decrease_cart_item, name='carts.minus'),
    path('increase_cart_item', views.increase_cart_item, name='carts.plus'),
]