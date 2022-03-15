from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils import timezone


class Post(models.Model):
    """ Model for making posts in the feed """
    content = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True,
                                      related_name='dislikes')

    def __str__(self):
        return f'{self.author}\'s post'


class Comment(models.Model):
    """ Model for commenting in posts detail view """
    comment = models.TextField(max_length=200)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Thread(models.Model):
    """ Model for DM thread created when users follow each other """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='+')

    """ Model for individual messages in a thread """
    thread = models.ForeignKey('Thread', related_name='+',
                               on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                      related_name='+')
    body = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)


class Friend(models.Model):
    """ Model for following users """
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner',
                                     on_delete=models.CASCADE, null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        """ handles following a user """
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def unfriend(cls, current_user, new_friend):
        """ handles removing a user from friend list"""
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)


class Notification(models.Model):
    """
    Model for handling various notificatins a user may receive
    #1 = like, 2 = comment, 3 = follow, 4= direct message, 5=event
    """

    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to',
                                on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from',
                                  on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE,
                             related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE,
                                related_name='+', blank=True, null=True)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE,
                               related_name='+', blank=True, null=True)
    event = models.ForeignKey('gig_calendar.Event', on_delete=models.CASCADE,
                              related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
