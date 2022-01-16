from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm, SetPasswordForm




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




# to override login form and add style tags
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-field'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-field'}))


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-field'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-field'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'form-field'}))
    
    
class PasswordChangeForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-field'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-field'}))