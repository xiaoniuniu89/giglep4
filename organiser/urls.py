from django.urls import path
from . import views as organiser_views
from .views import (
    post_create,
    post_update,
)
 
 
 
urlpatterns = [      
    path('feed/', organiser_views.feed, name='feed'),
    path('my-profile/', organiser_views.my_profile, name='my-profile'),
    path('feed/new/', post_create.as_view(), name='post-create'),
    path('feed/<int:pk>/update/', post_update.as_view(), name='post-update'),
 ]
 
