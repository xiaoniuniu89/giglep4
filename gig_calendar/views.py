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
    DeleteView
)
from .models import Event
from .utils import Calendar


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

