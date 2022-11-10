from django import forms
from django.forms import ModelForm

from .models import Member


from phonenumber_field.formfields import PhoneNumberField

class MemberForm(ModelForm):
    error_css_class = ' is-invalid'
    
    first_name = forms.CharField( required=True, widget=forms.TextInput(attrs={'class':'form-control '}))
    last_name = forms.CharField( required=True, widget=forms.TextInput(attrs={'class':'form-control '}))
    email = forms.EmailField( required=True, widget=forms.EmailInput(attrs={'class':'form-control '}))
    phone = PhoneNumberField( region="NG", widget=forms.TextInput(attrs={'class':'form-control '}))
    city = forms.CharField( required=True, widget=forms.TextInput(attrs={'class':'form-control '}))
    state = forms.CharField( required=True, widget=forms.TextInput(attrs={'class':'form-control '}))
    zip_code = forms.CharField( required=True, widget=forms.TextInput(attrs={'class':'form-control '}))

    class Meta:
        model = Member
        fields = "__all__"
