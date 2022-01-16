from django.urls import path
from . import views as social_views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, UserPasswordResetForm, PasswordChangeForm

urlpatterns = [
    path('', social_views.landing, name='landing-home'),
    path('sign-up/', social_views.sign_up, name='sign-up'),
    path('login/', auth_views.LoginView.as_view(template_name='landing/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', social_views.logout_view, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='landing/password_reset.html', form_class=UserPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='landing/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='landing/password_reset_confirm.html', form_class=PasswordChangeForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='landing/password_reset_complete.html'), name='password_reset_complete'),
    path('feed/', social_views.feed, name='feed'),
]