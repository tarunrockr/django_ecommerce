from django.shortcuts import render
from django.http import  HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from .models import Profile
from django.urls  import reverse
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from django.contrib.auth import  authenticate, login
import hashlib
from .import authentication
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def user_is_not_logged_in(user):
    return not user.is_authenticated

@user_passes_test(user_is_not_logged_in, login_url='/profiles/')
def showLogin(request):

    template = 'accounts/login.html'
    return render(request, template, {} )

@user_passes_test(user_is_not_logged_in, login_url='/profiles/')
def login_post(request):

    if request.method == 'POST':

        email     = request.POST['email']
        password  = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Storing userdata in session
            request.session['user_id']   = user.id
            request.session['logged_in'] = True
            request.session['email']     = user.email
            request.session['first_name']= user.first_name
            request.session['last_name'] = user.last_name

            auth.login(request, user)

            # Redirect to user profile
            return  HttpResponseRedirect(reverse('profile'))
        else:
            messages.error(request, "Error: Invalid credentials.")
            return HttpResponseRedirect(reverse('login.show'))
    else:
        return HttpResponseRedirect(reverse('login.show'))

@user_passes_test(user_is_not_logged_in, login_url='/profiles/')
def showRegister(request):

    templete = 'accounts/register.html'
    context = {}
    return render(request, templete, context)

@user_passes_test(user_is_not_logged_in, login_url='/profiles/')
def register(request):

    if request.method == 'POST':

        user_check = User.objects.filter(email=request.POST.get('email')).first()
        if user_check:
            messages.error(request, "Error: User already exists.")
            return HttpResponseRedirect(reverse('register.show'))
        else:

            first_name = request.POST.get('first_name')
            last_name  = request.POST.get('last_name')
            email      = request.POST.get('email')
            mobile     = request.POST.get('mobile')
            password   = request.POST.get('password')
            username   = get_random_string(length=6, allowed_chars='1234567890')

            user = User.objects.create_user( first_name=first_name, last_name=last_name, username=username, email=email, password=password )
            user.profile.mobile = mobile
            user.save()

            confirm_mail = email_confirmation(request, user.id, email)

            if user:
                messages.success(request, "Success: Registered successfully. <br> Check your email to activate account.")
                # messages.success(request, "Success: This is the sample success Flash message.")
                # messages.error(request, "Error: This is the sample error Flash message.")
                # messages.info(request, "Info: This is the sample info Flash message.")
                # messages.warning(request, "Warning: This is the sample warning Flash message.")
                return HttpResponseRedirect(reverse('register.show'))
            else:
                return HttpResponseRedirect(reverse('register.show'))
    else:
        templete = 'accounts/register.html'
        return render(request, templete, {})


def email_confirmation(request, user_id, email):

    # Working code without html subject

    # subject    = "E-Com email confirmation"
    # message    = "For confirmation of your mail click here"
    # from_email  = "info@ecom.com"
    # to_email   = [email]
    # #send_mail('<Your subject>', '<Your message>', 'from@example.com', ['to@example.com'])
    # send_mail( subject, message, from_email, to_email )
    # return True

    # With html template

    # Generating 32 digit random string
    random_string        = get_random_string(length=32)
    random_string_hash   = hashlib.md5(random_string.encode()).hexdigest()

    # Updating the user account with the hash
    user_account = User.objects.get(id=user_id)
    user_account.profile.hash = random_string_hash
    user_account.save()

    # msg = EmailMessage(subject, message, sender, to_list)
    subject              = "E-Com email confirmation"
    user_data            = User.objects.get(id=user_id)
    custom_url           = request.build_absolute_uri('/accounts/email_verification/'+random_string_hash+'/'+str(user_id)+'/')
    html_message         = render_to_string('emails/email_confirmation.html', {'user': user_data, 'hash': random_string_hash,'custom_url': custom_url})
    # plain_message        = strip_tags(html_message)
    from_email           = "info@ecom.com"
    to_email             = [email]
    msg                  = EmailMessage(subject, html_message, from_email, to_email)
    msg.content_subtype  = "html"  # Main content is now text/html
    return msg.send()

def email_verification(request, hash, user_id):

    # Fetching the user by hash and id
    user = User.objects.filter(id=user_id).first()
    if user:
        # Checking if already verified
        if user.profile.verified == 0:
            if user.profile.hash == hash:
                # Activate account by changing the status of verified in profile table
                user.profile.verified = 1
                user.save()
                messages.success(request, "Success: Email verified successfully. You can login now.")
                template = 'accounts/login.html'
                return render(request, template, {})
            else:
                messages.error(request, "Error: Link has been expired.")
                return HttpResponseRedirect(reverse('login.show'))
        else:
            messages.success(request, "Success: Email already verified.")
            return HttpResponseRedirect(reverse('login.show'))
    else:
        messages.error(request, "Error: User does not exists.")
        return HttpResponseRedirect(reverse('login.show'))

def logout(request):
    auth.logout(request)
    messages.success(request, "Success: Logout successfully.")
    return HttpResponseRedirect(reverse('login.show'))
