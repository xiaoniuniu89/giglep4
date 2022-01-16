from django.shortcuts import render
from django.http import HttpResponseRedirect, request
from django.http.response import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import MusicianUpdateForm, CommentForm
from django.contrib.auth.models import User
from social.forms import UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from .models import Post, Comment
from django.views import View
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
            return HttpResponseRedirect('/social/my-profile')
            
    else:
        user_form = UserUpdateForm(instance=request.user)
        musician_form = MusicianUpdateForm(instance=request.user.musician)
        
    
    context = {
        'user_form': user_form,
        'musician_form': musician_form,
    }
    
    return render(request, 'organiser/my-profile.html', context)


    
class post_create(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    success_url = '/social/feed/'
    success_message = 'Your post is now live ~ Who controls the present controls the past!'
    
    def form_valid(self, form):
        form.instance.author = self.request.user  # post author is form author set author before post is saved 
        return super().form_valid(form)



class post_update(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']
    success_url = '/social/feed/'
    success_message = 'Your post has been corrected ~ Who controls the past controls the future !'
    
    def form_valid(self, form):
        form.instance.author = self.request.user  # post author is form author set author before post is saved 
        return super().form_valid(form)
    
    
    # test user is author
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 

class post_delete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/social/feed/'
    success_message = 'Your post has been deleted ~ historical inaccuracy corrected!'
   
   
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(post_delete, self).delete(request, *args, **kwargs)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 


class post_detail(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        
        comments = Comment.objects.filter(post=post).order_by('-date_posted')

 
        
        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        
        return render(request, 'organiser/post_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            
        comments = Comment.objects.filter(post=post).order_by('-date_posted')
        
 
        
        context = {
            'post': post,
            'form': form,
            'comments': comments
        }
        
        return render(request, 'organiser/post_detail.html', context)