from django.test import TestCase, Client
from django.contrib.auth.models import User
from organiser.models import (
    Post,
    Comment,
    Thread,
    Message,
    Friend,
    Notification
)
from gig_calendar.models import Event


class TestModels(TestCase):
    """test organiser app models"""

    def setUp(self):
        """set up test variables"""
        self.client = Client()
        self.user1 = User.objects.create(
            username='test',
            email='test@email.com',
            password='test12344321',
        )
        self.client.force_login(self.user1)
        self.user2 = User.objects.create(
            username='test2',
            email='test2@email.com',
            password='test12344321',
        )
        self.post = Post.objects.create(
            author=self.user1,
            content='test content',
        )

    def test_user_has_post(self):
        """tests post can be created"""
        self.assertEquals(Post.objects.all().count(), 1)
        # test __str__
        self.assertEquals(str(self.post), 'test\'s post')

    def test_post_has_comment(self):
        """tests post can have comment"""
        Comment.objects.create(
            comment='test comment',
            author=self.user1,
            post=self.post
        )
        self.assertEquals(Comment.objects.all().count(), 1)
        # test __str__
        self.assertEquals(
            str(Comment.objects.get(
                pk=1)), 'test\'s comment on test\'s post\'s post')

    def test_post_has_like(self):
        """tests post can have like"""
        self.post.likes.add(self.user1)
        self.assertEquals(self.post.likes.count(), 1)

    def test_post_has_dislike(self):
        """tests post can have dislike"""
        self.post.dislikes.add(self.user1)
        self.assertEquals(self.post.dislikes.count(), 1)
       
    def test_user_has_thread(self):
        """tests post can be created"""
        Thread.objects.create(
            user=self.user1,
            receiver=self.user2
        )
        self.assertEquals(Thread.objects.all().count(), 1)
        # test __str__
        self.assertEquals(
            str(Thread.objects.get(
                pk=1)), 'Chat history between test and test2')

    def test_thread_has_message(self):
            """tests thread can have message"""
            thread = Thread.objects.create(
                user=self.user1,
                receiver=self.user2
            )
            msg = Message.objects.create(
            thread=thread,
            sender_user=self.user1,
            receiver_user=self.user2,
            body="this is a test message",
            is_read=False
            )
            self.assertEquals(Message.objects.all().count(), 1)
            # test __str__
            self.assertEquals(
                str(msg), 'message between test and test2')
    
    def test_user_has_friend(self):
        """tests user has friend"""
        self.assertEquals(Friend.objects.all().count(), 0)
        Friend.make_friend(self.user1, self.user2)
        self.assertEquals(Friend.objects.all().count(), 1)
        # test __str__
        self.assertEquals(str(Friend.objects.get(pk=1)), 'test\'s friends')
        
    def test_notification_created(self):
        """test notification creation"""

         # like notification
        Notification.objects.create(
            notification_type=1,
            post=self.post,
            to_user=self.user1,
            from_user=self.user2,
            user_has_seen=False
        )
        self.assertEquals(
            str(Notification.objects.get(
                pk=1)), 'Type 1 Notification from test2 to test')

        # comment notification
        Notification.objects.create(
            notification_type=2,
            post=self.post,
            to_user=self.user1,
            from_user=self.user2,
            user_has_seen=False
        )
        self.assertEquals(
            str(Notification.objects.get(
                pk=2)), 'Type 2 Notification from test2 to test')


       

        # follow notification
        Notification.objects.create(
            notification_type=3,
            to_user=self.user2,
            from_user=self.user1,
            user_has_seen=False
        )

        self.assertEquals(
            str(Notification.objects.get(
                pk=3)), 'Type 3 Notification from test to test2')

        # thread notification
        thread = Thread.objects.create(
                user=self.user1,
                receiver=self.user2
            )
        Notification.objects.create(
            notification_type=4,
            thread=thread,
            to_user=self.user2,
            from_user=self.user1,
            user_has_seen=False
        )

        self.assertEquals(
            str(Notification.objects.get(
                pk=4)), 'Type 4 Notification from test to test2')

        # event notification

        event = Event.objects.create(
            author=self.user1,
            title='test',
            description='test',
            date='2022-1-1'
        )
        self.event_not = Notification.objects.create(
            notification_type=5,
            event=event,
            to_user=self.user2,
            from_user=self.user1,
            user_has_seen=False
        )

        self.assertEquals(
            str(Notification.objects.get(
                pk=5)), 'Type 5 Notification from test to test2')



                
        