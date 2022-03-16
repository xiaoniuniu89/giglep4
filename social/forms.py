from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm
    )


class UserSignUpForm(UserCreationForm):
    """
    to add email to sign up form and
    override widget and add class
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-field'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-field'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-field'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-field'}))

    class Meta:
        """ form fields """
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    """
    override widget and add class for css
    """
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-field'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-field'}))


class UserUpdateForm(forms.ModelForm):
    """
    to addfirst & last name fields
    override widget and add class
    """
    first_name = forms.CharField(
        required=False, widget=forms.TextInput(
            attrs={'class': 'form-field'}))
    last_name = forms.CharField(
        required=False, widget=forms.TextInput(
            attrs={'class': 'form-field'}))

    class Meta:
        """ form fields """
        model = User
        fields = ['first_name', 'last_name']


class UserPasswordResetForm(PasswordResetForm):
    """ add class to form input """
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label='', widget=forms.EmailInput(
            attrs={'class': 'form-field'}))


class PasswordChangeForm(SetPasswordForm):
    """ add class to form inputs """
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-field'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-field'}))
