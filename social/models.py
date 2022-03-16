from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from cloudinary.models import CloudinaryField


# extends user model
class Musician(models.Model):
    """
    A musician is created through signals.py whenever
    a user signs up for an account
    """
    # delete profile for musician and not user account
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = CloudinaryField('image', default='placeholder')
    instrument = models.CharField(default='', max_length=50)
    location = models.CharField(default='', max_length=50)
    blurb = models.TextField(default='', max_length=100)

    # for admin page to display something other than musician object
    def __str__(self):
        return f'{self.user}\'s profile'
