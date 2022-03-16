import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Event(models.Model):
    """
    Model for events that will be populate
    the users calendar
    """
    author = models.ForeignKey(User, on_delete=CASCADE, default=None)
    title = models.CharField(max_length=20)
    description = models.TextField(default='')
    date = models.DateField(("Date"), default=datetime.date.today)

    def __str__(self):
        return f'{self.title} - {self.author}'
