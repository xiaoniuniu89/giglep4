from django.urls import path
from . import views as social_views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm

urlpatterns = [
    path('', social_views.landing, name='landing-home'),
    path('sign-up/', social_views.sign_up, name='sign-up'),
    path('login/', auth_views.LoginView.as_view(template_name='landing/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', social_views.logout_view, name='logout'),
]