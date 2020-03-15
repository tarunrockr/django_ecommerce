from django.urls import path
from .import views

urlpatterns=[
    path('', views.product_list, name='product.list'),
    path('product_detail/<int:id>/', views.product_detail, name='product.detail'),
    path('product_search_autocomplete', views.product_search_autocomplete, name='product.search.autocomplete'),
    path('product_search/', views.product_search, name='product.search'),
    path('product_list_ajax/', views.product_list_ajax, name="product.productlist.ajax"),
]