from django.test import SimpleTestCase
from django.urls import resolve, reverse
from organiser.views import (
    feed,
    post_create,
    post_update,
    post_delete,
    post_detail,
    comment_delete,
    add_like,
    dislike,
    change_friends,
    search_user,
    my_profile,
    user_profile,
    user_profile_list,
    list_thread,
    thread_view,
    create_message,
    post_notification,
    follow_notification,
    thread_notification,
    event_notification,
    remove_notification,
)

class TestUrls(SimpleTestCase):
    """URL tests for organiser app"""

    def test_feed_url_is_resolved(self):
        """feed url test"""
        url = reverse('feed')
        self.assertEquals(resolve(url).func.view_class, feed)

    def test_post_create_url_is_resolved(self):
        """post create url test"""
        url = reverse('post-create')
        self.assertEquals(resolve(url).func.view_class, post_create)

    def test_post_update_url_is_resolved(self):
        """post update url test"""
        url = reverse('post-update', args=[1])
        self.assertEquals(resolve(url).func.view_class, post_update)

    def test_post_delete_url_is_resolved(self):
        """post delete url test"""
        url = reverse('post-delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, post_delete)

    def test_post_detail_url_is_resolved(self):
        """post detail url test"""
        url = reverse('post-detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, post_detail)

    def test_comment_delete_url_is_resolved(self):
        """comment delete url test"""
        url = reverse('comment_delete', kwargs={'post_pk': 1, 'pk': 1})
        self.assertEquals(resolve(url).func.view_class, comment_delete)

    def test_like_url_is_resolved(self):
        """like url test"""
        url = reverse('like', args=[1])
        self.assertEquals(resolve(url).func.view_class, add_like)

    def test_dislike_url_is_resolved(self):
        """dislike url test"""
        url = reverse('dislike', args=[1])
        self.assertEquals(resolve(url).func.view_class, dislike)

    def test_change_friend_add_url_is_resolved(self):
        """add friends url test"""
        url = reverse('change_friends', kwargs={'operation': 'add', 'pk': 1})
        self.assertEquals(resolve(url).func, change_friends)

    def test_change_friend_remove_url_is_resolved(self):
        """remove friends url test"""
        url = reverse('change_friends', kwargs={'operation': 'remove', 'pk': 1})
        self.assertEquals(resolve(url).func, change_friends)

    def test_search_url_is_resolved(self):
        """search user url test"""
        url = reverse('search')
        self.assertEquals(resolve(url).func.view_class, search_user)

    def test_my_profile_url_is_resolved(self):
        """logged in user profile url test"""
        url = reverse('my-profile')
        self.assertEquals(resolve(url).func, my_profile)
    
    def test_user_profile_list_url_is_resolved(self):
        """user profile list url test"""
        url = reverse('user-profile-list')
        self.assertEquals(resolve(url).func.view_class, user_profile_list)

    def test_profile_url_is_resolved(self):
        """user profile/other users url test"""
        url = reverse('profile', args=[1])
        self.assertEquals(resolve(url).func.view_class, user_profile)
    
    def test_list_thread_url_is_resolved(self):
        """thread/inbox url test"""
        url = reverse('inbox')
        self.assertEquals(resolve(url).func.view_class, list_thread)
    
    def test_thread_view_url_is_resolved(self):
        """thread message url test"""
        url = reverse('thread', args=[1])
        self.assertEquals(resolve(url).func.view_class, thread_view)

    def test_create_message_url_is_resolved(self):
        """thread message create url test"""
        url = reverse('create_message', args=[1])
        self.assertEquals(resolve(url).func.view_class, create_message)

    def test_post_notification_url_is_resolved(self):
        """post notification url test"""
        url = reverse('post_notification', kwargs={'notification_pk': 1, 'post_pk': 1})
        self.assertEquals(resolve(url).func.view_class, post_notification)

    def test_follow_notification_url_is_resolved(self):
        """follow notification url test"""
        url = reverse('follow_notification', kwargs={'notification_pk': 1, 'profile_pk': 1})
        self.assertEquals(resolve(url).func.view_class, follow_notification)

    def test_thread_notification_url_is_resolved(self):
        """thread notification url test"""
        url = reverse('thread_notification', kwargs={'notification_pk': 1, 'object_pk': 1})
        self.assertEquals(resolve(url).func.view_class, thread_notification)

    def test_event_notification_url_is_resolved(self):
        """event notification url test"""
        url = reverse('event_notification', kwargs={'notification_pk': 1, 'object_pk': 1})
        self.assertEquals(resolve(url).func.view_class, event_notification)

    def test_remove_notification_url_is_resolved(self):
        """remove notification url test"""
        url = reverse('remove_notification', kwargs={'notification_pk': 1})
        self.assertEquals(resolve(url).func.view_class, remove_notification)