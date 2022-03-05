from django.shortcuts import render
from datetime import datetime, timedelta, date 
from django.utils.safestring import mark_safe
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import calendar
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
from organiser.models import User, Friend


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
    
    
    def form_valid(self, form):
        form.instance.author = self.request.user  # event author is form author set author before post is saved 
        return super().form_valid(form)
    
    
    # test user is author
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


class event_share(TemplateView):
    model = Event
    # model = User
    template_name = 'gig_calendar/event_share.html'
    
    def get_context_data(self, **kwargs):
        # context = super(event_share, self).get_context_data(**kwargs)
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
        
   

class event_share_confirm(TemplateView):
    model = Event
    # model = User
    template_name = 'gig_calendar/event_share_confirm.html'
    
    def get_context_data(self, **kwargs):
        # context = super(event_share, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context['from_user'] = User.objects.get(id=self.request.user.id)
        event = Event.objects.get(pk=kwargs['event_pk'])
        context['event'] = event
        to_user = User.objects.get(pk=kwargs['user_pk'])
        context['to_user'] = to_user
        return context
        
    
