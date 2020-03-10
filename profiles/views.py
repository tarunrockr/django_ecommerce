from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.models import  User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from  django.contrib import  messages


# Create your views here.
@login_required(login_url='/accounts/login/') # Redirect when user is not logged in
def profile(request):
    # if 'logged_in' in request.session:
    user_id = request.session['user_id']
    user_info = User.objects.get(pk=user_id)
    return  render(request, 'profiles/profile.html', {'user_data': user_info} )

    # return HttpResponseRedirect(reverse('login.show'))

@login_required(login_url='/accounts/login/') # Redirect when user is not logged in
def edit_profile(request):
    user_id = request.session['user_id']
    user_info = User.objects.get(pk=user_id)
    return render(request, 'profiles/edit_profile.html', {'user_data': user_info} )

@login_required(login_url='/accounts/login/') # Redirect when user is not logged in
def update_profile(request):

    form_type = request.POST.get('form_name')
    user_id   = request.POST.get('user_id')
    user      = User.objects.get(pk=user_id)

    if form_type == 'edit_first':
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email      = request.POST.get('email')
        mobile     = request.POST.get('mobile')

        user.first_name     = first_name
        user.last_name      = last_name
        user.profile.mobile = mobile
        user.save()

        messages.success(request, "Success: Profile updated successfully.")
        return  HttpResponseRedirect(reverse('profile.edit'))
    if form_type == 'edit_second':

        city        = request.POST.get('city')
        state       = request.POST.get('state')
        country     = request.POST.get('country')
        postal_code = request.POST.get('postal_code')

        user.profile.city        = city
        user.profile.state       = state
        user.profile.country     = country
        user.profile.postal_code = postal_code
        user.save()

        messages.success(request, "Success: Profile updated successfully.")
        return HttpResponseRedirect(reverse('profile.edit'))

    return HttpResponseRedirect(reverse('profile.edit'))




