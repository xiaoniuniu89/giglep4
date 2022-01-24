from django.test import TestCase
from social.models import Musician

class TestModels(TestCase):
    
    def setUp(self):
        self.client = Client()
        
        self.user1 = User.objects.create(
            username = 'test',
            email = 'test@email.com',
            password = 'test12344321',
        )