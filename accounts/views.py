from django.shortcuts import render
from django.http import  HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from .models import Profile
from django.urls  import reverse
from django.utils.crypto import get_random_string
from django.contrib import messages

# Create your views here.

def showLogin(request):

    template = 'accounts/login.html'
    context = {}
    return render(request, template, context)

def showRegister(request):

    templete = 'accounts/register.html'
    context = {}
    return render(request, templete, context)

def register(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email      = request.POST.get('email')
        mobile     = request.POST.get('mobile')
        password   = request.POST.get('password')
        username     = get_random_string(length=6, allowed_chars='1234567890')
        print(first_name)

        print(email)
        user = User.objects.create_user( first_name=first_name, last_name=last_name, username=username, email=email, password=password )
        user.profile.mobile = mobile
        user.save()

        if user:
            messages.success(request, "Success: Registered successfully.")
            # messages.success(request, "Success: This is the sample success Flash message.")
            # messages.error(request, "Error: This is the sample error Flash message.")
            # messages.info(request, "Info: This is the sample info Flash message.")
            # messages.warning(request, "Warning: This is the sample warning Flash message.")
            return HttpResponseRedirect(reverse('register.show'))
        else:
            return HttpResponseRedirect(reverse('register.show'))
    else:
        templete = 'accounts/register.html'
        context = {}
        return render(request, templete, context)