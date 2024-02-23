from django import forms
from .models import ContactUs
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name', 'email']



class ContactUsForm(forms.ModelForm):
    class Meta:
        model=ContactUs
        fields='__all__'