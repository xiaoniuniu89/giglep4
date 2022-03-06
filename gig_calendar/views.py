from django.shortcuts import render, redirect
from datetime import datetime, timedelta, date 
from django.utils.safestring import mark_safe
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, request
from django.contrib import messages
from django.db.models import Q
import calendar
from django.views import View
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from .models import Event
from .utils import Calendar
from .forms import EventForm
from organiser.models import User, Friend, Notification


class CalendarView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'gig_calendar/calendar.html'

    def get_context_data(self, **kwargs):
        user = self.request.user.id
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(user, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
    

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month



class event_create(SuccessMessageMixin, LoginRequiredMixin, CreateView): #LoginRequiredMixin add this later
    model = Event
    fields = ['title', 'date', 'description']
    success_url = '/calendar/'
    success_message = 'Event added!'
    
    
    def form_valid(self, form):
        form.instance.author = self.request.user  # event author is form author set author before post is saved 
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = EventForm()
        return context


class event_detail_view(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Event


    # test user is author
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 

class event_list_view(LoginRequiredMixin, ListView):
    model = Event

    template_name = 'gig_calendar/event_list.html'
    
    
    def get_context_data(self, **kwargs):
        context = super(event_list_view, self).get_context_data(**kwargs)
        
        context["events"] = Event.objects.filter(date__year=self.kwargs["slug_year"], date__month=self.kwargs["slug_month"], date__day=self.kwargs["slug_day"], author=self.request.user)
        return context



class event_update(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView): #LoginRequiredMixin UserPassesTestMixin and test_func
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
    
    
    def form_valid(self, form):
        form.instance.author = self.request.user  # event author is form author set author before post is saved 
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 
    
    
class event_delete(LoginRequiredMixin, UserPassesTestMixin, DeleteView): #UserPassesTestMixin
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
    model = Event
    template_name = 'gig_calendar/event_share.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(id=self.request.user.id)
        event = Event.objects.get(pk=kwargs['pk'])
        context['event'] = event
        try:
            friend_obj = Friend.objects.get(current_user=self.request.user)
            context['friends'] = friend_obj.users.all()
        except Friend.DoesNotExist:
            context['friends'] = None
        return context

    def test_func(self, **kwargs):
        event = Event.objects.get(pk=self.kwargs['pk'])
        if self.request.user == event.author:
            return True
        return False

    
        
   

class event_share_confirm(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View):
    model = Event
    template_name = 'gig_calendar/event_share_confirm.html'

    def get(self, request, *args, **kwargs):
        
        context = {
            'to_user': User.objects.get(pk=kwargs['user_pk']),
            'event': Event.objects.get(pk=kwargs['event_pk']),
            'from_user': User.objects.get(id=self.request.user.id)
        }

        return render(request, 'gig_calendar/event_share_confirm.html', context)

    def test_func(self, **kwargs):
        event = Event.objects.get(pk=self.kwargs['event_pk'])
        to_user = User.objects.get(pk=self.kwargs['user_pk'])
        from_user = User.objects.get(id=self.request.user.id)
        friends = Friend.objects.get(current_user=from_user).users.all()
        # friends = friend_obj.users.all()
        if self.request.user == event.author and to_user in friends:
            return True
        return False

            

    def post(self, request, *args, **kwargs):
        to_user =  User.objects.get(pk=kwargs['user_pk'])
        event = Event.objects.get(pk=kwargs['event_pk'])
        from_user = User.objects.get(id=self.request.user.id)

        notification = Notification.objects.create(
            notification_type=5,
            from_user=from_user,
            to_user=to_user,
            event=event
        )
        if to_user.first_name == '':
            messages.success(request, f'Event shared with {to_user.username}!')
        else:
            messages.success(request, f'Event shared with {to_user.first_name}!')
        return redirect('cal:calendar')
    
        
class event_invite(View):
    model = Event
    template_name = 'gig_calendar/event_invite.html'


    def get(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs['pk'])
        user_events = Event.objects.filter(Q(date=event.date) & Q(author=request.user))
        
        context = {
            'event': event,
            'user_events': user_events
        }

        return render(request, 'gig_calendar/event_invite.html', context)

            

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs['pk'])
        Event.objects.create(
            author=self.request.user,
            title=event.title,
            description=event.description,
            date=event.date
        )

        messages.success(request, 'Event added to calendar!')
        return redirect('feed')


