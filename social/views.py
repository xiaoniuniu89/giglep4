from django.shortcuts import render, redirect
from .forms import UserSignUpForm
from django.contrib import messages

def landing(request):
    return render(request, 'landing/landing.html')

def login(request):
    return render(request, 'landing/login.html')

def sign_up(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}, you can now login!')
            return redirect('login')
    else:
        form = UserSignUpForm()
       
        
    return render(request, 'landing/sign-up.html', {'form': form})
