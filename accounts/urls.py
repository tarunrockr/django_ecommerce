from django.urls import path
from .import views

urlpatterns=[
    path('', views.showLogin, name='login.show'),
    path('login/', views.showLogin, name='login.show.login'),
    path('register/', views.showRegister, name='register.show'),
    path('register/post', views.register, name='register'),
]