from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    # if request.user.is_authenticated():
    #     username = 'Uri Boyka'
    #     context={'username': username}
    # else:
    #     context={'username': 'unknown'}

    context = {'username': 'unknown'}

    template = 'products/index.html'
    return render(request, template, context )


