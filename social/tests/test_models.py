from django.test import TestCase, Client
from social.models import Musician
from django.contrib.auth.models import User


class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        
        self.user1 = User.objects.create(
            username = 'test',
            email = 'test@email.com',
            password = 'test12344321',
        )

    def test_user_has_profile(self):
        self.assertEquals(self.user1.musician.user.username, 'test')