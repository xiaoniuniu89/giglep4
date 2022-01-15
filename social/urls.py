from django.urls import path
from . import views as social_views

urlpatterns = [
    path('', social_views.landing, name='landing-home'),
    path('sign-up/', social_views.sign_up, name='sign-up'),
]