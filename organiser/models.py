from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils import timezone


class Post(models.Model):
    """
    Model for making posts in the feed
    Help re likes and dislikes from
    https://www.youtube.com/watch?v=NRexdRbvd6o&list=
    PLPSM8rIid1a3TkwEmHyDALNuHhqiUiU5A&index=7
    """
    content = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True,
                                      related_name='dislikes')

    def __str__(self):
        return f'{self.author}\'s post'

    class Meta:
        """ordering by date posted - newest first"""
        ordering = ['-date_posted']


class Comment(models.Model):
    """ Model for commenting in posts detail view """
    comment = models.TextField(max_length=200)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}\'s comment on {self.post}\'s post'


class Thread(models.Model):
    """
    Model for DM thread created when users follow each other
    With help from:
    https://www.youtube.com/watch?v=oxrQdZ5KqW0&list=
    PLPSM8rIid1a3TkwEmHyDALNuHhqiUiU5A&index=15
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='+')

    def __str__(self):
        return f'Chat history between {self.user} and {self.receiver}'


class Message(models.Model):
    """
    Model for individual messages in a thread
    With help from:
    https://www.youtube.com/watch?v=oxrQdZ5KqW0&list=
    PLPSM8rIid1a3TkwEmHyDALNuHhqiUiU5A&index=15
    """
    thread = models.ForeignKey('Thread', related_name='+',
                               on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                      related_name='+')
    body = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'message between {self.sender_user} and {self.receiver_user}'


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

    def __str__(self):
        return f'{self.current_user}\'s friends'


class Notification(models.Model):
    """
    Model for handling various notificatins a user may receive
    #1 = like, 2 = comment, 3 = follow, 4= direct message, 5=event
    Help from this tutorial
    https://www.youtube.com/watch?v=_JKWYkz597c&t=4s
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

    def __str__(self):
        return f'Type {self.notification_type} Notification from {self.from_user} to {self.to_user}'
