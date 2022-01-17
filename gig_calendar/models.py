from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE 
import datetime
from django.conf import settings

# Create your models here.

class Event(models.Model):
    author = models.ForeignKey(User, on_delete=CASCADE, default=None)
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    date = models.DateField(("Date"), default=datetime.date.today)
    
    def __str__(self):
        return self.title