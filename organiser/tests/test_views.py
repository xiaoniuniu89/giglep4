import datetime
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from organiser.models import (
    Post,
    Comment,
    Friend,
    Thread,
    Message,
    Notification,
)
from gig_calendar.models import Event

from organiser.views import (
    feed,
    post_create,
    post_update,
    post_delete,
    post_detail,
    comment_delete,
    my_profile,
    user_profile_list,
    user_profile,
)


class TestViews(TestCase):
    """Test organiser app views"""

    def setUp(self):
        """ set up test variables"""
        self.client = Client()
        self.factory = RequestFactory()
        # make a user
        self.user1 = User.objects.create(
            username='test',
            email='test@email.com',
        )
        # log user1 in
        self.client.force_login(self.user1)
        # a friend to interact with
        self.user2 = User.objects.create(
            username='test2',
            email='test2@email.com',
            password='test12344321',
        )
        # a friend to interact with
        self.user3 = User.objects.create(
            username='test3',
            email='test3@email.com',
            password='test12344321',
        )
        # user1 and 2 are friends
        Friend.make_friend(self.user1, self.user2)
        # post to interact with
        self.post1 = Post.objects.create(
            author=self.user1,
            content='test content',
        )
        # give post a like
        self.post1.likes.add(self.user2)
        # post to interact with
        self.post2 = Post.objects.create(
            author=self.user2,
            content='test content two',
        )
        # give post dislikes
        self.post2.dislikes.add(self.user1)
        self.post2.dislikes.add(self.user2)
        # comment for testing
        self.comment = Comment.objects.create(
            comment='test comment',
            author=self.user2,
            post=self.post1
        )
        # thread to interact with
        self.thread = Thread.objects.create(
            user=self.user1,
            receiver=self.user2
        )
        # message to interact with
        self.message = Message.objects.create(
            thread=self.thread,
            sender_user=self.user1,
            receiver_user=self.user2,
            body="this is a test message",
            is_read=False
        )
        # event to interact with
        self.event = Event.objects.create(
            author=self.user1,
            title='title',
            description='test',
            date='2022-01-01'
        )

        # comment notification
        self.com_not = Notification.objects.create(
            notification_type=2,
            post=self.comment.post,
            to_user=self.user1,
            from_user=self.user2,
            user_has_seen=False
        )

        # like notification
        self.like_not = Notification.objects.create(
            notification_type=1,
            post=self.comment.post,
            to_user=self.user1,
            from_user=self.user2,
            user_has_seen=False
        )

        # follow notification
        self.fol_not = Notification.objects.create(
            notification_type=3,
            to_user=self.user2,
            from_user=self.user1,
            user_has_seen=False
        )

        # thread notification
        self.thread_not = Notification.objects.create(
            notification_type=4,
            thread=self.thread,
            to_user=self.user2,
            from_user=self.user1,
            user_has_seen=False
        )

        # event notification
        self.event_not = Notification.objects.create(
            notification_type=5,
            event=self.event,
            to_user=self.user2,
            from_user=self.user1,
            user_has_seen=False
        )

        # urls
        self.feed_url = reverse('feed')
        self.post_create_url = reverse('post-create')
        self.post_update_url = reverse('post-update', args=[1])
        self.post_delete_url = reverse('post-delete', args=[self.post1.pk])
        self.post_detail_url = reverse('post-detail', args=[self.post1.pk])
        self.comment_delete_url = reverse(
            'comment_delete', kwargs={
                'post_pk': self.post1.pk, 'pk': self.comment.pk})
        self.like_url = reverse('like', args=[1])
        self.dislike_url = reverse('dislike', args=[1])
        # test will make friends with user 3
        self.add_friend_url = reverse(
            'change_friends', kwargs={
                'operation': 'add', 'pk': self.user3.pk})
        # test will remove user2 from friends
        self.remove_friend_url = reverse(
            'change_friends', kwargs={
                'operation': 'remove', 'pk': self.user2.pk})
        self.search_user_url = reverse('search')
        self.my_profile_url = reverse('my-profile')
        # looking at user1 friend list
        self.user_profile_list_url = reverse('user-profile-list')
        # user1 looking at user 2 profile
        self.user_profile_url = reverse('profile', args=[2])
        self.list_thread_url = reverse('inbox')
        self.thread_url = reverse('thread', args=[1])
        self.create_message_url = reverse('create_message', args=[1])
        self.post_notification_url = reverse(
            'post_notification', kwargs={
                'notification_pk': 1, 'post_pk': self.post1.pk})
        self.follow_notification_url = reverse(
            'follow_notification', kwargs={
                'notification_pk': 3, 'profile_pk': self.user2.pk})
        self.thread_notification_url = reverse(
            'thread_notification', kwargs={
                'notification_pk': 4, 'object_pk': self.thread.pk})
        self.event_notification_url = reverse(
            'event_notification', kwargs={
                'notification_pk': 4, 'object_pk': self.event.pk})
        self.event_invite_url = reverse(
                    'cal:event_invite', args=[1])
        self.remove_notification_url = reverse(
            'remove_notification', args=[1])

    # feed
    def test_feed_get(self):
        """ test feed get """
        request = self.factory.get(self.feed_url)
        request.user = self.user1
        response = feed.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_feed_context(self):
        """ test feed context data """
        request = self.factory.get(self.feed_url)
        request.user = self.user1
        response = feed.as_view()(request)
        self.assertTrue(
            self.user3 in response.context_data[
                'user_you_may_know'])
        self.assertTrue(
            self.post1 in response.context_data[
                'posts'])
        self.assertTrue(
            self.post2 in response.context_data[
                'posts'])
        self.assertEquals(self.post1.likes.all().count(), 1)
        self.assertEquals(self.post2.dislikes.all().count(), 2)

    # create post
    def test_create_post_get(self):
        """create post get test"""
        request = self.factory.get(self.post_create_url)
        request.user = self.user1
        response = post_create.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_create_post_post(self):
        """test post submit response code"""
        response = self.client.post(self.post_create_url, {
            'author': self.user1.username,
            'content': 'tests are exciting'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, self.feed_url)
        posts_by_user = Post.objects.filter(author=self.user1)
        # 1 from setUP and 1 from newly created post
        self.assertEquals(len(posts_by_user), 2)

    # edit post
    def test_edit_post_get(self):
        """update post get test"""
        request = self.factory.get(self.post_update_url)
        request.user = self.user1
        response = post_update.as_view()(request, pk=1)
        self.assertEquals(response.status_code, 200)

    def test_update_post_post(self):
        """update post submit response code"""
        response = self.client.post(self.post_update_url, {
            'author': self.user1.username,
            'content': 'tests are very exciting'
        }, follow=True, pk=1)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, self.feed_url)

    # delete post
    def test_delete_post_get(self):
        """update post get test"""
        request = self.factory.get(self.post_delete_url)
        request.user = self.user1
        response = post_delete.as_view()(request, pk=1)
        self.assertEquals(response.status_code, 200)

    def test_delete_post_post(self):
        """delete post submit response code"""
        response = self.client.post(
            self.post_delete_url, follow=True, pk=1)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, self.feed_url)
        posts_by_user = Post.objects.filter(
            author=self.user1)
        # 1 from setUP and 0 after delete
        self.assertEquals(len(posts_by_user), 0)

    # post detail
    def test_post_detail_get(self):
        """ post detail get response test"""
        request = self.factory.get(self.post_detail_url)
        request.user = self.user1
        response = post_detail.as_view()(request, pk=1)
        self.assertEquals(response.status_code, 200)

    def test_post_detail_post(self):
        """ post detail POST data test"""
        response = self.client.post(self.post_detail_url, {
            'comment': 'test comment',
            'author': self.user2,
            'post': self.post1
        }, follow=True, pk=1)
        self.assertEquals(response.status_code, 200)
        comments = Comment.objects.filter(post=self.post1)
        # 1 from setUp 1 just created
        self.assertEquals(len(comments), 2)

    # delete comment
    def test_delete_comment_get(self):
        """delete post commnet get test"""
        self.client.force_login(self.user2)
        request = self.factory.get(self.comment_delete_url)
        request.user = self.user2
        response = comment_delete.as_view()(
            request, post_pk=1, pk=1)
        self.assertEquals(response.status_code, 200)

    def test_delete_comment_post(self):
        """delete post comment code"""
        self.client.force_login(self.user2)
        response = self.client.post(
            self.comment_delete_url, follow=True, post_pk=1, pk=1)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, self.post_detail_url)
        comments = Comment.objects.filter(
            author=self.user2, post=self.post1)
        # user 2 has deleted their comment made in setup
        self.assertEquals(len(comments), 0)

    # likes and dislikes
    def test_likes_add(self):
        """add a like test"""
        self.client.force_login(self.user3)
        response = self.client.post(
            self.like_url, follow=True, pk=1)
        # 1 from set up and 1 just created by user 3
        self.assertEquals(self.post1.likes.all().count(), 2)

    def test_likes_remove(self):
        """add a like test"""
        self.client.force_login(self.user3)
        response = self.client.post(
            self.dislike_url, follow=True, pk=1)
        # 0 from set up and 1 after dislike
        self.assertEquals(self.post1.dislikes.all().count(), 1)

    # adding and removing friends
    def test_friend_add(self):
        """add a friend test"""
        response = self.client.post(self.add_friend_url, follow=True)
        friend_obj = Friend.objects.get(current_user=self.user1)
        # user 3 added to friends of user 1
        self.assertTrue(self.user3 in friend_obj.users.all())

    def test_friend_remove(self):
        """remove a friend test"""
        response = self.client.post(self.remove_friend_url, follow=True)
        friend_obj = Friend.objects.get(current_user=self.user1)
        # user2 removed from user1 friends
        self.assertFalse(self.user2 in friend_obj.users.all())

    # search users
    def test_search_user(self):
        """search user test """
        response = self.client.get(self.search_user_url, {
            'user': self.user2.username
        })
        # user 2 is recorded in the search query
        self.assertTrue(self.user2 in response.context.get(
            'object_list'))

    # my profile
    def test_my_profile_get(self):
        """ logged in user profile test """
        request = self.factory.get(self.my_profile_url)
        request.user = self.user1
        response = my_profile(request)
        self.assertEquals(response.status_code, 200)

    def test_my_profile_post(self):
        """ test my profile post/ update profile """
        response = self.client.post(self.my_profile_url, {
            'first_name': 'test',
            'last_name': 'ing',
            'instrument': 'python',
            'location': 'the cloud',
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, self.my_profile_url)
        self.assertEquals(
            response.context['user'].musician.instrument, 'python')

    # user profile list
    def test_user_profile_list_get(self):
        """ test friends list get """
        request = self.factory.get(self.user_profile_list_url)
        request.user = self.user1
        response = user_profile_list.as_view()(request)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(
            self.user2 in response.context_data[
                'friends'])

    # user profile
    def test_user_profile_get(self):
        """ test friends list get """
        request = self.factory.get(self.user_profile_url)
        request.user = self.user1
        response = user_profile.as_view()(request, pk=self.user2.pk)
        self.assertEquals(response.status_code, 200)
        # true because user1 is looking at user 2 profile
        self.assertTrue(
            self.user2 in response.context_data[
                'friends'])

    # user inbox
    def test_inbox_get(self):
        """ test inbox get """
        response = self.client.get(self.list_thread_url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.thread in response.context['threads'])
        # testing a profile card containing user2s username
        # is present in the html
        self.assertTrue(bytes(
            self.user2.username, encoding='utf8') in response.content)

    # thread DM
    def test_thread_get(self):
        """ test thread get """
        response = self.client.get(self.thread_url, pk=self.thread.pk)
        self.assertEquals(response.status_code, 200)
        # testing message in thread
        self.assertTrue(self.message in response.context['message_list'])

    # creating message
    def test_create_message_post(self):
        """ test create a new message """
        response = self.client.post(self.create_message_url, {
            'body': 'test'}, pk=self.thread.pk, follow=True)
        self.assertEquals(response.status_code, 200)
        # 1 from setup and 1 just created
        self.assertEquals(response.context['message_list'].count(), 2)

    # notifications
    def test_post_notification_comment(self):
        """ test comment on post notification """
        response = self.client.get(
            self.post_notification_url,
            notification_pk=self.com_not.pk,
            post_pk=self.post1.pk, follow=True
        )
        # post renders and redirects to post detail page
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, self.post_detail_url)

    def test_post_notification_like(self):
        """ test comment on post notification """
        response = self.client.get(
            self.post_notification_url,
            notification_pk=self.like_not.pk,
            post_pk=self.post1.pk, follow=True
        )
        # post renders and redirects to post detail page
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, self.post_detail_url)

    def test_follow_notification(self):
        """ test follow notification """
        response = self.client.get(
            self.follow_notification_url,
            notification_pk=self.fol_not.pk,
            profile_pk=self.user2.pk, follow=True
        )
        # redirects to user who followed profile page
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, self.user_profile_url)

    def test_thread_notification(self):
        """ test thread notification """
        response = self.client.get(
            self.thread_notification_url,
            notification_pk=self.thread_not.pk,
            object_pk=self.thread.pk,
            follow=True
        )
        # redirects to thread page
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, self.thread_url)

    def test_event_notification(self):
        """ test event notification """
        response = self.client.get(
            self.event_notification_url,
            notification_pk=self.event_not.pk,
            object_pk=self.event.pk,
            follow=True
        )
        #  redirects to event invite page
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, self.event_invite_url)
