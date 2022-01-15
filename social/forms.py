from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



# to add email to sign up form 
class UserSignUpForm(UserCreationForm):
    # override and add class
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-field'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-field'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-field'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-field'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']