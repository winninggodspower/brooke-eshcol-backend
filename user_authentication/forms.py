
from django import forms
from django.forms import ModelForm 
from django.contrib.auth.forms import UserCreationForm

from .models import Subscriber

# import the model here to populate the form
from django.contrib.auth import get_user_model
User = get_user_model()

def validate_email(email):
    if not User.objects.filter(email = email).first():
        raise forms.ValidationError('Incorrect email or password')


def email_available(email):
    if User.objects.filter(email = email).first():
        raise forms.ValidationError('Email already taken. if yours, proceed to login')


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=70, validators= [validate_email])
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)

    email.widget.attrs.update({'class' : 'form-control border-0 border-bottom rounded-0', 'placeholder': 'Email'})
    password.widget.attrs.update({'class' : 'form-control border-0 border-bottom rounded-0','placeholder': 'Password'})


class RegisterForm(UserCreationForm):

    error_css_class = ' is-invalid'

    password1 = forms.CharField(required=True, widget = forms.PasswordInput(attrs={'class' : 'form-control border-0 border-bottom rounded-0', 'placeholder':'Choose Password'}))
    password2 = forms.CharField(required=True, widget = forms.PasswordInput(attrs={'class' : 'form-control border-0 border-bottom rounded-0', 'placeholder':'Comfirm password'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control border-0 border-bottom rounded-0', 'placeholder':'Email adress', 'required': 'true'}),
            validators=[email_available])
    class Meta:
        model = User
        # specify field to be displayed from model here
        fields = ('username','email','password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control border-0 border-bottom rounded-0', 'placeholder':'Email', 'required': 'true'}),
            'username': forms.TextInput(attrs={'class':'form-control border-0 border-bottom rounded-0', 'placeholder':'Name'}),
        }


    def save(self, commit = True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user

class SubscriberForm(ModelForm):
    email = forms.EmailField( required=True, widget=forms.EmailInput(attrs={'class':'form-control rounded-0 text-light'}))
    class Meta:
        model = Subscriber
        fields = ('email',)

    # email = forms.EmailField(label='Your email',
    #                          max_length=100,
    #                          widget=forms.EmailInput(attrs={'class': 'form-control rounded-0 text-light'}))

