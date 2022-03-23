from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestViews(TestCase):
    """ Test landing app views"""

    def setUp(self):
        """ set up testing variables """
        self.client = Client()
        self.landing_url = reverse('landing-home')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.sign_up_url = reverse('sign-up')

        self.user1 = User.objects.create(
            username='test',
            email='test@email.com',
            password='test12344321',
        )

    def test_landing_GET(self):
        """test landing page response code"""
        response = self.client.get(self.landing_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/landing.html')

    def test_login_GET(self):
        """test login page response code"""
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/login.html')

    def test_logout_GET(self):
        """test logout page response code"""
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_sign_up_GET(self):
        """test sign up page get response code"""
        response = self.client.get(self.sign_up_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/sign-up.html')

    def test_sign_up_POST(self):
        """test sign up page post response code"""
        # making a fake post
        response = self.client.post(self.sign_up_url, {
            'username': 'test1',
            'email': 'test@email.com',
            'password1': 'test12344321',
            'password2': 'test12344321'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/')
        self.assertEquals(self.user1.musician.user.username, 'test')

    def test_sign_up_POST_no_data(self):
        """test sign up page no data response code"""
        # make fake post with no data
        response = self.client.post(self.sign_up_url, {
            'username': '',
            'email': '',
            'password1': '',
            'password2': ''
        })

        self.assertEquals(response.status_code, 200)
