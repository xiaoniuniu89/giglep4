from django.test import TestCase, Client
from django.contrib.auth.models import User
from gig_calendar.models import Event


class TestModels(TestCase):
    """test calendar app model Event"""
    def setUp(self):
        """set up test variables"""
        self.client = Client()
        self.user1 = User.objects.create(
            username='test',
            email='test@email.com',
            password='test12344321',
        )

        self.event = Event.objects.create(
            author=self.user1,
            title='title',
            description='test',
            date='2022-01-01'
        )

    def test_user_has_event(self):
        """test users can create events"""
        self.assertEquals(self.event.author, self.user1)
        self.assertEquals(Event.objects.all().count(), 1)
