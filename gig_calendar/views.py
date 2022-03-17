import calendar
import random
from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from organiser.models import User, Friend, Notification
from .models import Event
from .utils import Calendar
from .forms import EventForm


class CalendarView(LoginRequiredMixin, ListView):
    """
    Uses calendar class from utils.py to display
    a html calendar with users events
    """
    model = Event
    template_name = 'gig_calendar/calendar.html'

    def get_context_data(self, **kwargs):
        user = self.request.user.id
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        # initialise calendar with this months year and date
        cal = Calendar(d.year, d.month)
        # returns html calendar as a table
        html_cal = cal.formatmonth(user, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_month):
    """
    Helper function for calendar view
    to return correct date for calendar
    """
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    """
    Helper function for calendar view
    to return previous months date
    """
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    """
    Helper function for calendar view
    to return next months date
    """
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class event_create(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Create view for making events to add to calendar
    """
    model = Event
    fields = ['title', 'date', 'description']
    success_url = '/calendar/'
    success_message = 'Event added!'

    def form_valid(self, form):
        """
        event author is form author/set author before post is saved
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = EventForm()
        return context


class event_detail_view(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Event detail view - uses django generic view
    """
    model = Event

    # test user is author
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class event_list_view(LoginRequiredMixin, ListView):
    """
    List view for events in case user has
    multiple events on the same day
    """
    model = Event
    template_name = 'gig_calendar/event_list.html'

    def get_context_data(self, **kwargs):
        context = super(event_list_view, self).get_context_data(**kwargs)
        context["events"] = Event.objects.filter(
            date__year=self.kwargs["slug_year"],
            date__month=self.kwargs["slug_month"],
            date__day=self.kwargs["slug_day"],
            author=self.request.user
        )
        return context


class event_update(
    SuccessMessageMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    """
    Event update view - uses django generic view
    """
    model = Event
    id = Event.pk
    fields = ['title', 'date', 'description']
    success_url = '/calendar/'
    success_message = 'Event updated!'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        event = Event.objects.get(pk=pk)
        context = super().get_context_data(**kwargs)
        context["form"] = EventForm(instance=event)
        return context

    # event author is form author set author before post is saved
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class event_delete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Event delete view - uses django generic view
    """
    model = Event
    success_url = '/calendar/'
    success_message = 'Event Deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(event_delete, self).delete(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class event_share(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    view for sharing events with other users
    information is passed from the event detail to here,
    then information from this view is passed to event
    confirmation view
    """
    model = Event
    template_name = 'gig_calendar/event_share.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_suggestion = User.objects.exclude(id=self.request.user.id)
        # get event id from url
        event = Event.objects.get(pk=kwargs['pk'])
        context['event'] = event
        # get friends list to choose who to pass event to
        # check has friends
        try:
            friend_obj = Friend.objects.get(current_user=self.request.user)
            friends = friend_obj.users.all().order_by('username')
            # 0 if user had at least 1 friend that they unfollowed
            if len(friends) == 0:
                friend_suggestion = User.objects.exclude(id=self.request.user.id)
                context['user_you_may_know'] = random.sample(list(
                    friend_suggestion), 4)
        except Friend.DoesNotExist:
            friends = None
        # paginate the results
        paginator = Paginator(friends, 6)
        page_number = self.request.GET.get('page')
        try:
            context['friends'] = paginator.get_page(page_number)
        except TypeError:
            # friends object is empty if user has never had a friend
            context['friends'] = None
            friend_suggestion = User.objects.exclude(id=self.request.user.id)
            context['user_you_may_know'] = random.sample(list(
                    friend_suggestion), 4)
        return context

    # test user wrote the event
    def test_func(self, **kwargs):
        event = Event.objects.get(pk=self.kwargs['pk'])
        if self.request.user == event.author:
            return True
        return False


class event_share_confirm(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    View
):
    """
    This view collects informatin from event share view
    for user to confirm. Upon sending all of the information about
    who sent the event and the event details, it is sent
    via a notification for the invitee to accept - upon accepting
    the event, it is recreated in the invitees calendar with the only
    change being the author will be set to the invitee
    """
    model = Event
    template_name = 'gig_calendar/event_share_confirm.html'

    def get(self, request, *args, **kwargs):
        # important information to be passed in notification
        # so the invitee can save event in their own calendar
        context = {
            # kwargs are in the url
            'to_user': User.objects.get(pk=kwargs['user_pk']),
            'event': Event.objects.get(pk=kwargs['event_pk']),
            'from_user': User.objects.get(id=self.request.user.id)
        }

        return render(
            request,
            'gig_calendar/event_share_confirm.html',
            context
        )

    def test_func(self, **kwargs):
        event = Event.objects.get(pk=self.kwargs['event_pk'])
        to_user = User.objects.get(pk=self.kwargs['user_pk'])
        from_user = User.objects.get(id=self.request.user.id)
        friends = Friend.objects.get(current_user=from_user).users.all()
        if self.request.user == event.author and to_user in friends:
            return True
        return False

    def post(self, request, *args, **kwargs):
        """
        culmination of the past 2 views - from user
        to user and event details passed in the
        notification
        """
        to_user = User.objects.get(pk=kwargs['user_pk'])
        event = Event.objects.get(pk=kwargs['event_pk'])
        from_user = User.objects.get(id=self.request.user.id)

        notification = Notification.objects.create(
            notification_type=5,
            from_user=from_user,
            to_user=to_user,
            event=event
        )
        if to_user.first_name == '':
            messages.success(
                request,
                f'Event shared with {to_user.username}!'
            )
        else:
            messages.success(
                request,
                f'Event shared with {to_user.first_name}!'
            )
        return redirect('cal:calendar')


class event_invite(View):
    """
    Information here is passed from the notification and if the user
    accepts then a the event information will be stored in the database
    but the event author will be set to the logged in user
    """
    model = Event
    template_name = 'gig_calendar/event_invite.html'

    def get(self, request, *args, **kwargs):
        """ Get event info """
        # kwargs in url
        event = Event.objects.get(pk=kwargs['pk'])
        user_events = Event.objects.filter(
            Q(date=event.date) & Q(
                author=request.user
            )
        )

        context = {
            'event': event,
            'user_events': user_events
        }

        return render(request, 'gig_calendar/event_invite.html', context)

    def post(self, request, *args, **kwargs):
        """ save event info to calendar """
        event = Event.objects.get(pk=kwargs['pk'])
        Event.objects.create(
            # copy data & change author
            author=self.request.user,
            title=event.title,
            description=event.description,
            date=event.date
        )

        messages.success(request, 'Event added to calendar!')
        return redirect('feed')
