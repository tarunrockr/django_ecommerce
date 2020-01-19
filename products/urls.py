from django.urls import path
from .import views

urlpatterns=[
    path('', views.product_list, name='Product.list'),
    path('product_detail/<int:id>/', views.product_detail, name='product.detail'),
]