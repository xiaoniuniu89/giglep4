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


class feed(LoginRequiredMixin, ListView):
    """
    Logic for feed page
    paginates posts by 6 per page
    also displays 4 random users to follow
    """
    paginate_by = 6
    model = Post
    template_name = 'organiser/feed.html'

    def get_context_data(self, **kwargs):
        context = super(feed, self).get_context_data(**kwargs)
        # step1 get users
        context['users'] = User.objects.exclude(id=self.request.user.id)

        try:
            # step2 try find any friends
            friend_obj = Friend.objects.get(current_user=self.request.user)
            friends = friend_obj.users.all()
            context['friends'] = friends
            friend_suggestion = User.objects.exclude(
                id__in=friends).exclude(id=self.request.user.id)
            try:
                # step 3 if available - suggest 4 friends
                context['user_you_may_know'] = random.sample(list(
                    friend_suggestion), 4)
            except ValueError:
                # incase not 4 return all
                context['user_you_may_know'] = random.sample(list(
                    friend_suggestion), len(friend_suggestion))
            # return posts
            context['posts'] = Post.objects.filter(
                Q(author=self.request.user) | Q(
                    author__in=friends))

        except Friend.DoesNotExist:
            # if user has no friends
            context['friends'] = None
            friend_suggestion = User.objects.exclude(id=self.request.user.id)
            context['user_you_may_know'] = friend_suggestion.all()[:4]
            context['posts'] = Post.objects.filter(author=self.request.user)
        return context


class post_create(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Post create logic - uses create view to handle heavy lifting
    upon creation will redirect back to feed
    create post buttonin feed
    """
    model = Post
    fields = ['content']
    success_url = '/social/feed/'
    success_message = '''Your post is now live ~
    Who controls the present controls the past!'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm()
        return context

    def form_valid(self, form):
        # post author is form author/set author before post is saved
        form.instance.author = self.request.user
        return super().form_valid(form)


class post_update(
    SuccessMessageMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    """
    update posts - use update view
    edit post button in feed template
    """

    model = Post
    fields = ['content']
    success_url = '/social/feed/'
    success_message = '''Your post has been corrected ~
    Who controls the past controls the future !'''

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=post)
        return context

    def form_valid(self, form):
        # post author is form author/set author before post is saved
        form.instance.author = self.request.user
        return super().form_valid(form)

    # test request user is author
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class post_delete(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):

    """
    delete the post - uses inbuilt delete view
    """

    model = Post
    success_url = '/social/feed/'
    success_message = '''Your post has been deleted ~
    historical inaccuracy corrected!'''

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(post_delete, self).delete(request, *args, **kwargs)

    # check logged in user is author
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class post_detail(LoginRequiredMixin, View):
    """
    Post detail view
    is customized to also display comments
    """
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        # get commonets for the post
        comments = Comment.objects.filter(
            post=post).order_by('-date_posted')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(
            request, 'organiser/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        """ Handles posting a comment in post detail """
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by(
            '-date_posted')

        # to give 1 notification for multiple unseen comments
        # from same user on same post
        if not Notification.objects.filter(Q(post=post) & Q(
            from_user=request.user) & Q(
                user_has_seen=False)).exists():
            notification = Notification.objects.create(
                notification_type=2,
                from_user=request.user,
                to_user=post.author,
                post=post)

        context = {
            'post': post,
            'form': form,
            'comments': comments
        }

        return render(request, 'organiser/post_detail.html', context)


class comment_delete(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):

    """ Delete view - use inbuilt delete view to delete comment """

    model = Comment
    template_name = 'organiser/comment_confirm_delete.html'
    success_message = 'Your comment has been deleted!'

    # bring back to post associated with comment
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(comment_delete, self).delete(request, *args, **kwargs)

    # test logged in user is comment author
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


class add_like(LoginRequiredMixin, View):
    """
    Handles logic to add likes
    on a post - will check if user has liked
    or dislike already before updating
    A lot of help from the following tutorial

    https://www.youtube.com/watch?v=NRexdRbvd6o&list=
    PLPSM8rIid1a3TkwEmHyDALNuHhqiUiU5A&index=7

    """
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
    """
    Handles logic to remove likes
    on a post - will check if user has liked
    or dislike already before updating
    A lot of help from the following tutorial

    https://www.youtube.com/watch?v=NRexdRbvd6o&list=
    PLPSM8rIid1a3TkwEmHyDALNuHhqiUiU5A&index=7
    """
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

def change_friends(request, operation, pk):
    """
    Logic to handle follow and unfollow
    if user clicks follow the operation pass
    add as operation and vice versa
    Also includes logic to create a new thread
    when a user first follows someone or is
    followed by someone else
    """

    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
        # if there is a thread return it
        if Thread.objects.filter(
            user=request.user,
            receiver=friend
        ).exists():
            thread = Thread.objects.filter(
                user=request.user, receiver=friend)[0]
        elif Thread.objects.filter(
            user=friend, receiver=request.user
        ).exists():
            thread = Thread.objects.filter(
                user=friend, receiver=request.user)[0]
        else:
            # if there is no thread, make one
            thread = Thread(
                        user=request.user,
                        receiver=friend
                    )
            thread.save()
    elif operation == 'remove':
        Friend.unfriend(request.user, friend)

    # create 1 notification - avoid problem
    # of user following and unfollowing many
    # times
    if not Notification.objects.filter(Q(
        notification_type=3) & Q(
            from_user=request.user) & Q(
                to_user=friend) & Q(
                    user_has_seen=False)).exists():
        notification = Notification.objects.create(
            notification_type=3,
            from_user=request.user,
            to_user=friend)

    return redirect('feed')

class search_user(ListView):
    """
    Will display a list of users from searchbar search term
    and display in a list - users are searchable by username
    and first and last name

    Help from the following tutorial

    https://www.youtube.com/watch?v=yDJZk761Iik&list=
    PLPSM8rIid1a3TkwEmHyDALNuHhqiUiU5A&index=8
    """
    model = User
    template_name = 'organiser/search_results.html'
    context_object_name = 'users'

    def get_queryset(self):
        try:
            acc = self.request.GET.get('user',).lstrip().rstrip().split(
                " ")[0]
        except KeyError:
            # if no user logged in
            acc = None
        if acc:
            account_list = User.objects.filter(Q(
                username__icontains=acc) | Q(
                    first_name__icontains=acc) | Q(last_name__icontains=acc))
        else:
            account_list = User.objects.filter(username=self.request.user)
        return account_list




@login_required
def my_profile(request):
    """
    logic to handle logged in user profile
    it uses two forms - user and musician -
    to update users information
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        musician_form = MusicianUpdateForm(
            request.POST, request.FILES, instance=request.user.musician)

        if user_form.is_valid() and musician_form.is_valid():
            user_form.save()
            musician_form.save()
            messages.success(
                request, 'Profile has been updated successfully')
            return HttpResponseRedirect('/social/my-profile')

    else:
        # on errors, prev filled in data or on first loading
        user_form = UserUpdateForm(instance=request.user)
        musician_form = MusicianUpdateForm(instance=request.user.musician)

    context = {
        'user_form': user_form,
        'musician_form': musician_form,
    }

    return render(request, 'organiser/my-profile.html', context)


class user_profile_list(ListView):
    """
    Logic for displaying logged in user friends list
    """
    model = User
    template_name = 'organiser/profile_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(
            id=self.request.user.id)

        try:
            friend_obj = Friend.objects.get(
                current_user=self.request.user)
            friends = friend_obj.users.all().order_by(
                'username')
        except Friend.DoesNotExist:
            friends = None
        paginator = Paginator(friends, 6)

        page_number = self.request.GET.get('page')
        context['friends'] = paginator.get_page(page_number)
        return context


class user_profile(DetailView):
    """
    Used to display profile of any user
    other than currently logged in user
    """
    model = User
    template_name = 'organiser/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(id=self.request.user.id)
        try:
            # if friends will display a chat button
            context['threads'] = Thread.objects.filter(
                Q(user=self.request.user) | Q(receiver=self.request.user))

        except Thread.DoesNotExist:
            context['threads'] = None

        try:
            # if friends: will display an unfollow/chat button
            friend_obj = Friend.objects.get(current_user=self.request.user)
            context['friends'] = friend_obj.users.all()
        except Friend.DoesNotExist:
            # if not friend will display a follow button only
            context['friends'] = None
        return context


class list_thread(View):

    """
    Displays a list of any conversations user has -
    A conversation is created automatically when a user
    follows another user - threads have a user and a
    receiver - dependant on who is the follower and
    who received the follower
    """

    def get(self, request, *args, **kwargs):
        threads_obj = Thread.objects.filter(Q(
            user=request.user) | Q(
                receiver=request.user)).order_by('pk')
        paginator = Paginator(threads_obj, 6)

        page_number = request.GET.get('page')
        threads = paginator.get_page(page_number)
        context = {
            'threads': threads,
        }

        return render(request, 'organiser/inbox.html', context)


class thread_view(View):
    """
    This is the DM view - each thread is associated with a
    message list that is displayed here
    With help from:
    https://www.youtube.com/watch?v=oxrQdZ5KqW0&list=
    PLPSM8rIid1a3TkwEmHyDALNuHhqiUiU5A&index=15
    """
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
    """
    Handles writing a message in the thread view/DM
    A conversation is created automatically when a user
    follows another user - threads have a user and a
    receiver - dependant on who is the follower and
    who received the follower
    """
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
        # 1 notification for multiple msg from 1 user
        if not Notification.objects.filter(Q(
            thread=thread) & Q(
                user_has_seen=False)).exists():
            notification = Notification.objects.create(
                notification_type=4,
                from_user=request.user,
                to_user=receiver,
                thread=thread
            )

        return redirect('thread', pk=pk)


class post_notification(View):
    """
    Notifications are in gigle template tags
    Upon clicking notification it is removed
    and user is taken to the post

    Help from this tutorial
    https://www.youtube.com/watch?v=_JKWYkz597c&t=4s
    """
    def get(
        self,
        request,
        notification_pk,
        post_pk,
        *args,
        **kwargs
    ):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post-detail', pk=post_pk)


class follow_notification(View):
    """
    Notifications are in gigle template tags
    Upon clicking notification it is removed
    and user is taken to the profile of user who
    just followed logged in user

    Help from this tutorial
    https://www.youtube.com/watch?v=_JKWYkz597c&t=4s
    """
    def get(
        self,
        request,
        notification_pk,
        profile_pk,
        *args,
        **kwargs
    ):

        notification = Notification.objects.get(pk=notification_pk)
        profile = User.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', pk=profile_pk)


class thread_notification(View):
    """
    Notifications are in gigle template tags
    Upon clicking notification it is removed
    and user is taken to DM associated
    with the notification

    Help from this tutorial
    https://www.youtube.com/watch?v=_JKWYkz597c&t=4s
    """
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = Thread.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=object_pk)


class event_notification(View):
    """
    Notifications are in gigle template tags
    Upon clicking notification it is removed
    and user is taken to a page to accept or decline
    the event

    Help from this tutorial
    https://www.youtube.com/watch?v=_JKWYkz597c&t=4s
    """
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        event = Event.objects.get(pk=object_pk)
        notification.user_has_seen = True
        notification.save()

        return redirect('cal:event_invite', pk=object_pk)


class remove_notification(View):
    """
    Lets user close notification without going to the page
    associated with the notification

    Help from this tutorial
    https://www.youtube.com/watch?v=_JKWYkz597c&t=4s
    """
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        notification.save()
        return HttpResponse('success', content_type='text/plain')
