from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string


# modules needed for user authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#for pasword reset
from django.contrib.auth import views
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

#for verifying email
from verify_email.email_handler import send_verification_email


from django.conf import settings

# importing the use model
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Subscriber #importing the newsletter model

# importing the forms
from .forms import LoginForm, RegisterForm, SubscriberForm

# Create your views here.

def home(request):
    newsLetterForm = SubscriberForm()
    return render(request, 'index.html', {'newsletterForm': newsLetterForm})

def services(request):
    newsLetterForm = SubscriberForm()
    return render(request, 'services.html', {'newsletterForm': newsLetterForm})

def courses(request):
    return render(request, 'courses.html')


# routes for user registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            # form.save only works when form is created from a model
            inactive_user = send_verification_email(request, form)
            # print(inactive_user.cleaned_data['email']); print(inactive_user.cleaned_data)

            # form.save()
            messages.success(request, 'succesfully created account')
            return redirect('verification_email_sent')
        else:

            # adding the is-invalid class to field with errors
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'

            # rendering the template again if the form is not valid with the prepopulated data.
            return render(request, 'signup.html', {'form': form})

    else:
        form = RegisterForm()
        return render(request, 'signup.html', {'form': form})


def login_user(request):
    # redirect user to home if already logged in
    if request.user.is_authenticated:
        messages.info(request, 'You Are Already Logged In')
        return redirect('/home')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = User.objects.filter(email = form.cleaned_data.get('email')).first()
            # the authenticate function returns the user object if the user is found else it returns none
            user = authenticate(username=username, password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                messages.success(request, 
                f'successfully logged in as {user.username}')
                return redirect('/home')

            else:
                # adding the is-invalid class to field with errors
                for field in form.errors:
                    form[field].field.widget.attrs['class'] += ' is-invalid'

                messages.error(request, 'Invalid credentials')
                # form.add_error('user not found')
                return redirect('/login')

        # if form is not valid render the template again with pre populated data
        else:
            return render(request, 'signin.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'signin.html', {'form': form})


@login_required
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'successfully logged out')
        return redirect('/home')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    email_content = {
                    "email": user.email,
                    'domain': settings.DOMAIN,
                    'site_name': settings.SITE_NAME,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': settings.PROTOCOL,
                    }
                    email = render_to_string(email_template_name, email_content)
                    try:
                        send_mail(subject, email, 'contact@brookeeshcol.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
            else:
                messages.error(request, 'email not found in our database')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})



def newSubscriber(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # checking if email has already been subscribed to news letter
        if Subscriber.objects.filter(email = email):
                messages.error(request, "Email already subscribed to our newsletter")
                return redirect('home')

        sub = SubscriberForm(request.POST)
        if sub.is_valid():
           
            messages.success(request, "You've succcessfully subcribed to our newsletter")
            sub.save()
        else:
            for error in sub.errors.as_json():
                print(error)

            messages.error(request, "invalid email address")
        
    return redirect('home')

def verification_email_sent(request):
    return render(request, "verify_email/email_sent.html")


def error_404_view(request, exception):
       
    # we add the path to the the 404.html file
    return render(request, '404.html')