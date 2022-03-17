from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from social.views import landing, logout_view, sign_up


class TestUrls(SimpleTestCase):
    """Test social landing app urls"""

    def test_landing_home_is_resolved(self):
        """test landing page resolves"""
        url = reverse('landing-home')
        self.assertEquals(resolve(url).func, landing)

    def test_sign_up_is_resolved(self):
        """test sign p page resolves"""
        url = reverse('sign-up')
        self.assertEquals(resolve(url).func, sign_up)

    def test_login_view_is_resolved(self):
        """test login page resolves"""
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_is_resolved(self):
        """test logout page resolves"""
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_view)

    def test_pass_reset_is_resolved(self):
        """test password reset page resolves"""
        url = reverse('password_reset')
        self.assertEquals(
            resolve(url).func.view_class,
            auth_views.PasswordResetView
        )

    def test_pass_reset_done_is_resolved(self):
        """test password reset done resolves"""
        url = reverse('password_reset_done')
        self.assertEquals(
            resolve(url).func.view_class,
            auth_views.PasswordResetDoneView
        )

    def test_pass_reset_confirm_is_resolved(self):
        """test password reset confirm resolves"""
        url = reverse('password_reset_confirm', args=[1234, 1234])
        self.assertEquals(
            resolve(url).func.view_class,
            auth_views.PasswordResetConfirmView
        )

    def test_pass_reset_complete_is_resolved(self):
        """test password reset complete resolves"""
        url = reverse('password_reset_complete')
        self.assertEquals(
            resolve(url).func.view_class,
            auth_views.PasswordResetCompleteView
        )
