from django.test import TestCase, Client
from django.contrib.auth.models import User


class TestModels(TestCase):
    """test social app user model"""

    def setUp(self):
        """set up test variables"""
        self.client = Client()
        self.user1 = User.objects.create(
            username='test',
            email='test@email.com',
            password='test12344321',
        )

    def test_user_has_profile(self):
        """tests signal to create musician profile works"""
        self.assertEquals(self.user1.musician.user.username, 'test')
        # test __str__
        self.assertEquals(str(self.user1.musician), 'test\'s profile')
