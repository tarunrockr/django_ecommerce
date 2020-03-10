from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# Create your models here.

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile      = models.TextField()
    city        = models.CharField(max_length=50)
    state       = models.CharField(max_length=50)
    country     = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    hash        = models.TextField(null=True)
    verified    = models.IntegerField(default='0', editable=False)
    created_at  = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at  = models.DateTimeField(auto_now_add=False, auto_now=True)
    status      = models.IntegerField(default=1)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()