from django.urls import path
from . import views as social_views

urlpatterns = [
    path('', social_views.landing, name='landing-home'),
   
]