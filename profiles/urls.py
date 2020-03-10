from django.urls import path
from .import views

urlpatterns=[
    path('', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='profile.edit'),
    path('update/', views.update_profile, name='profile.update')
]