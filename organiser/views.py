from django.shortcuts import render
from django.http import HttpResponseRedirect, request
from django.http.response import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import MusicianUpdateForm
from django.contrib.auth.models import User
from social.forms import UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

# Create your views here.



def feed(request):
    return render(request, 'organiser/feed.html')


@login_required
def my_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        musician_form = MusicianUpdateForm(request.POST, request.FILES, instance=request.user.musician)
        
        if user_form.is_valid() and musician_form.is_valid():
            user_form.save()
            musician_form.save()
            messages.success(request, 'Profile has been updated successfully')
            return HttpResponseRedirect('/organiser/my-profile')
            
    else:
        user_form = UserUpdateForm(instance=request.user)
        musician_form = MusicianUpdateForm(instance=request.user.musician)
        
    
    context = {
        'user_form': user_form,
        'musician_form': musician_form,
    }
    
    return render(request, 'organiser/my-profile.html', context)
