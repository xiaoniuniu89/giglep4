from django.urls import path
from . import views as organiser_views
 
 
 
urlpatterns = [      
    path('', organiser_views.feed, name='feed'),
 ]
 
