from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, request
import random
from django.http.response import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import MusicianUpdateForm, CommentForm, MessageForm, PostForm
from django.contrib.auth.models import User
from social.forms import UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from .models import Post, Comment, Thread, Message, Friend, Notification
from gig_calendar.models import Event
from django.views import View
from django.db.models import Q
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
    paginate_by = 6
    model = Post
    template_name = 'organiser/feed.html'
    
    
    
    def get_context_data(self, **kwargs):
        context = super(feed, self).get_context_data(**kwargs)
        
        context['users'] = User.objects.exclude(id=self.request.user.id)
        try:
            friend_obj = Friend.objects.get(current_user=self.request.user)
            friends = friend_obj.users.all()
            context['friends'] = friends
            friend_suggestion = User.objects.exclude(id__in = friends).exclude(id=self.request.user.id)
            try:
                context['user_you_may_know'] = random.sample(list(friend_suggestion), 4)
            except ValueError as e:
                context['user_you_may_know'] = random.sample(list(friend_suggestion), len(friend_suggestion))
            context['posts'] = Post.objects.filter(Q (author=self.request.user) | Q (author__in =  friends)).order_by('-date_posted')

        except Friend.DoesNotExist:
            context['friends'] = None
            friend_suggestion = User.objects.exclude(id=self.request.user.id)
            context['user_you_may_know'] = friend_suggestion.all()[:4]
            context['posts'] = Post.objects.filter(author=self.request.user)
            
        # context['posts'] = Post.objects.filter(Q (author=self.request.user) | Q (author__in =  friends)).order_by('-date_posted')
        # context['poster'] = posts.filter(Q (author=self.request.user) | Q (author__in =  friends)).order_by('-date_posted')

        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        users = User.objects.exclude(id=self.request.user.id)
        try:
            friend_obj = Friend.objects.get(current_user=self.request.user)
            friends = friend_obj.users.all()
            # context['friends'] = friends
        except Friend.DoesNotExist:
            pass
            friends = []
        filter_list = Post.objects.filter(Q (author=self.request.user) | Q (author__in =  friends)).order_by('-date_posted')
        return filter_list
    




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
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(id=self.request.user.id)
        try:
            context['threads'] = Thread.objects.filter(Q(user=self.request.user) | Q(receiver=self.request.user))

        except Thread.DoesNotExist:
            context['threads'] = None
      
        
        try:
            friend_obj = Friend.objects.get(current_user=self.request.user)
            context['friends'] = friend_obj.users.all()
        except Friend.DoesNotExist:
            context['friends'] = None
        return context
    
class post_create(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    success_url = '/social/feed/'
    success_message = 'Your post is now live ~ Who controls the present controls the past!'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user  # post author is form author set author before post is saved 
        return super().form_valid(form)



class post_update(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']
    success_url = '/social/feed/'
    success_message = 'Your post has been corrected ~ Who controls the past controls the future !'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=post)
        return context
    
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
        if not Notification.objects.filter(Q(post=post) & Q(from_user=request.user) & Q (user_has_seen = False)).exists():
            notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)

        
 
        
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


class list_thread(View):
    def get(self, request, *args, **kwargs):
        threads_obj = Thread.objects.filter(Q(user=request.user) | Q(receiver=request.user)).order_by()
        paginator = Paginator(threads_obj, 6) 

        page_number = request.GET.get('page')
        threads = paginator.get_page(page_number)
        context = {
            'threads': threads,
            
        }
        
        return render(request, 'organiser/inbox.html', context)


class thread_view(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = Thread.objects.get(pk=pk)
        message_list = Message.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'message_list': message_list, 
            'form': form
        }
        
        return render(request, 'organiser/thread.html', context)

class create_message(View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = Thread.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else: 
            receiver = thread.receiver
            
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()
        if not Notification.objects.filter(Q(thread=thread) & Q (user_has_seen = False)).exists():
            notification = Notification.objects.create(
                notification_type=4,
                from_user=request.user,
                to_user=receiver,
                thread=thread
            )
            
        
        return redirect('thread', pk=pk)



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
    
    if not Notification.objects.filter(Q(notification_type=3) & Q(from_user=request.user) & Q(to_user=friend) & Q(user_has_seen = False)).exists():    
        notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=friend)
   
           
    return redirect('feed')

class user_profile_list(ListView):
    model = User
    template_name = 'organiser/profile_list.html'
    # paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(id=self.request.user.id)
        

        try:
            friend_obj = Friend.objects.get(current_user=self.request.user)
            friends = friend_obj.users.all().order_by('username')
            # context['friends'] = friends
        except Friend.DoesNotExist:
            # context['friends'] = None
            friends = None
        paginator = Paginator(friends, 6)

        page_number = self.request.GET.get('page')
        context['friends'] = paginator.get_page(page_number)
        return context


class add_like(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        
        is_dislike = False 
        
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True 
                break 
            
        if is_dislike:
            post.dislikes.remove(request.user)
            
        is_like = False 
        
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
            
        if not is_like:
            post.likes.add(request.user)
          
            
            
        if is_like:
            post.likes.remove(request.user)
        
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
            
            
class dislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        
        
        is_like = False 
        
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
            
        if is_like:
            post.likes.remove(request.user)
            
        is_dislike = False 
        
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True 
                break 
        
        if not is_dislike:
            post.dislikes.add(request.user)
            
        if is_dislike:
            post.dislikes.remove(request.user)
            
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
        
        

class post_notification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)
        
        notification.user_has_seen = True
        notification.save()
        
        return redirect('post-detail', pk=post_pk)
    
    
class follow_notification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = User.objects.get(pk=profile_pk)
        
        notification.user_has_seen = True
        notification.save()
        
        return redirect('profile', pk=profile_pk)
    
class thread_notification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = Thread.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()
        
        return redirect('thread', pk=object_pk)

class event_notification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        event = Event.objects.get(pk=object_pk)
        notification.user_has_seen = True
        notification.save()
        
        return redirect('cal:event_invite', pk=object_pk)


class remove_notification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        notification.save()
        return HttpResponse('success', content_type='text/plain')
        

class search_user(ListView):
    model = User
    template_name = 'organiser/search_results.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        try:
            acc = self.request.GET.get('user',).lstrip().rstrip().split(" ")[0]
        except KeyError:
            acc = None
        if acc:
            account_list = User.objects.filter(Q(username__icontains=acc) | Q(first_name__icontains=acc) | Q(last_name__icontains=acc))
        else:
            account_list = User.objects.filter(username=self.request.user)
        return account_list