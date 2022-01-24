from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from social.models import Musician

class TestViews(TestCase):


    def setUp(self):
        self.client = Client()
        self.landing_url = reverse('landing-home')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.sign_up_url = reverse('sign-up')
        
        self.user1 = User.objects.create(
            username = 'test',
            email = 'test@email.com',
            password = 'test12344321',
        )
        

    def test_landing_GET(self):
        response = self.client.get(self.landing_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing/landing.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing/login.html')


    def test_logout_GET(self):
        response = self.client.get(self.logout_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_sign_up_GET(self):
        response = self.client.get(self.sign_up_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing/sign-up.html')

    def test_sign_up_POST(self):
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
        response = self.client.post(self.sign_up_url, {
            'username': '',
            'email': '',
            'password1': '',
            'password2': ''
        })

        self.assertEquals(response.status_code, 200)
        


    


        
        

    