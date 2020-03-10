from django.urls import path
from .import views

urlpatterns=[
    path('', views.showLogin, name='login.show'),
    path('login/', views.showLogin, name='login.show.login'),
    path('login/post/', views.login_post, name='login.post'),
    path('register/', views.showRegister, name='register.show'),
    path('register/post', views.register, name='register'),
    path('email_verification/<slug:hash>/<int:user_id>/', views.email_verification, name='email.verify'),
    path('logout/', views.logout, name='logout')
]