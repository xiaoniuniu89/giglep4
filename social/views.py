from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserSignUpForm


def landing(request):
    """ landing home page view"""
    return render(request, 'landing/landing.html')


def login(request):
    """
    login view, uses django auth views
    """
    return render(request, 'landing/login.html')


def logout_view(request):
    """
    logout view, uses django auth views
    """
    logout(request)
    messages.info(request, f'Logged out!')
    return redirect('landing-home')


def sign_up(request):
    """
    sign-up view
    """
    if request.method == 'POST':
        # custom form
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            # form validation
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username}, you can now login!')
            return redirect('login')
    else:
        form = UserSignUpForm()

    return render(request, 'landing/sign-up.html', {'form': form})
