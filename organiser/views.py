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
from django.urls.base import reverse_lazy
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

# Create your views here.


class feed(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'organiser/feed.html'
    paginate_by = 6




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

class user_profile(DetailView):
    model = User
    template_name = 'organiser/profile.html'
    
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

class comment_delete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'organiser/comment_confirm_delete.html'
    success_message = 'Your comment has been deleted!'
    
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})
   
   
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(comment_delete, self).delete(request, *args, **kwargs)
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False 


def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
        if Thread.objects.filter(user=request.user, receiver=friend).exists():
            thread = Thread.objects.filter(user=request.user, receiver=friend)[0]
        elif Thread.objects.filter(user=friend, receiver=request.user).exists():
            thread = Thread.objects.filter(user=friend, receiver=request.user)[0]
        else:
            thread = Thread(
                        user=request.user, 
                        receiver=friend
                    ) 
            thread.save()
    elif operation == 'remove':
        Friend.unfriend(request.user, friend)
        
        
    notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=friend)
           
    return redirect('feed')