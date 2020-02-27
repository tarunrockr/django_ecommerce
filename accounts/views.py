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

        confirm_mail = email_confirmation(user.id,email)

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


def email_confirmation(user_id, email):

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
    

    # msg = EmailMessage(subject, message, sender, to_list)
    subject              = "E-Com email confirmation"
    user_data            = User.objects.get(id=user_id)
    html_message         = render_to_string('emails/email_confirmation.html', {'user': user_data})
    plain_message        = strip_tags(html_message)
    from_email           = "info@ecom.com"
    to_email             = [email]
    msg                  = EmailMessage(subject, plain_message, from_email, to_email)
    msg.content_subtype  = "html"  # Main content is now text/html
    return msg.send()