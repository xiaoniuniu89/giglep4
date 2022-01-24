from django.test import SimpleTestCase
from django.urls import reverse, resolve 
from social.views import landing, login, logout_view, sign_up
from django.contrib.auth import views as auth_views


class TestUrls(SimpleTestCase):

    def test_landing_home_is_resolved(self):
        url = reverse('landing-home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, landing)

    def test_sign_up_is_resolved(self):
        url = reverse('sign-up')
        print(resolve(url))
        self.assertEquals(resolve(url).func, sign_up)

    def test_login_view_is_resolved(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_is_resolved(self):
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func, logout_view)

    def test_pass_reset_is_resolved(self):
        url = reverse('password_reset')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetView)

    def test_pass_reset_done_is_resolved(self):
        url = reverse('password_reset_done')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_pass_reset_confirm_is_resolved(self):
        url = reverse('password_reset_confirm', args=[1234, 1234])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)

    def test_pass_reset_complete_is_resolved(self):
        url = reverse('password_reset_complete')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)

    