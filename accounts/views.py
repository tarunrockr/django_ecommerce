from django.shortcuts import render
from django.http import  HttpResponse, Http404, JsonResponse

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
    print('in register post')
    if request.POST == 'POST':

    else:
        templete = 'accounts/register.html'
        context = {}
        return render(request, templete, context)