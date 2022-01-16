from django.urls import path
from . import views as organiser_views
from .views import (
    post_create,
    post_update,
    post_delete,
    post_detail,
    comment_delete,
)
 
 
 
urlpatterns = [      
    path('feed/', organiser_views.feed, name='feed'),
    path('my-profile/', organiser_views.my_profile, name='my-profile'),
    path('feed/new/', post_create.as_view(), name='post-create'),
    path('feed/<int:pk>/update/', post_update.as_view(), name='post-update'),
    path('feed/<int:pk>/delete/', post_delete.as_view(), name='post-delete'),
    path('feed/<int:pk>/view/', post_detail.as_view(), name='post-detail'),
    path('feed/<int:post_pk>/comment/delete/<int:pk>/', comment_delete.as_view(), name='comment_delete'),



 ]
 
