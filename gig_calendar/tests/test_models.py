from django.test import TestCase, Client
from gig_calendar.models import Event
from django.contrib.auth.models import User


class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        
        self.user1 = User.objects.create(
            username = 'test',
            email = 'test@email.com',
            password = 'test12344321',
        )
        
        self.event = Event.objects.create(
            author = self.user1,
            title = 'title',
            description = 'test',
            date = '2022-01-01'
        )


    def test_user_has_event(self):
        self.assertEquals(self.event.author, self.user1)