from django.urls import path
from . import views as organiser_views
 
 
 
urlpatterns = [      
    path('feed/', organiser_views.feed, name='feed'),
    path('my-profile/', organiser_views.my_profile, name='my-profile'),

 ]
 
