from django.urls import path
from . import views as calendar_views


app_name = 'cal'

urlpatterns = [

    path('', calendar_views.CalendarView.as_view(), name='calendar'),
    path('event/new/', calendar_views.event_create.as_view(), name='event-create'),
    path('event/<int:pk>/', calendar_views.event_detail_view.as_view(), name='event_detail'),



]

