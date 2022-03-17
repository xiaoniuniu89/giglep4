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
from organiser.views import (
    feed,
    post_create,
    post_update,
    post_delete,
    post_detail,

)

class TestViews(TestCase):
    """Test organiser app views"""

    def setUp(self):
        """ set up test variables"""
        self.client = Client()
        self.factory = RequestFactory()

        self.user1 = User.objects.create(
            username = 'test',
            email = 'test@email.com',
        )
        self.client.force_login(self.user1)

        self.user2 = User.objects.create(
            username = 'test2',
            email = 'test2@email.com',
            password = 'test12344321',
        )

        self.user3 = User.objects.create(
            username = 'test3',
            email = 'test3@email.com',
            password = 'test12344321',
        )

        Friend.make_friend(self.user1, self.user2)
        
        self.post1 = Post.objects.create(
            author = self.user1,
            content = 'test content',
        )
        self.post1.likes.add(self.user2)

        self.post2 = Post.objects.create(
            author = self.user2,
            content = 'test content two',
        )

        self.post2.dislikes.add(self.user1)
        self.post2.dislikes.add(self.user2)

        self.comment = Comment.objects.create(
            comment = 'test comment',
            author = self.user2,
            post = self.post1
        )


        # urls
        self.feed_url = reverse('feed')
        self.post_create_url = reverse('post-create')
        self.post_update_url = reverse('post-update', args=[1])
        self.post_delete_url = reverse('post-delete', args=[self.post1.pk])
        self.post_detail_url = reverse('post-detail', args=[self.post1.pk])

    # feed view

    def test_feed_GET(self):
        request = self.factory.get(self.feed_url)
        request.user = self.user1
        response = feed.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_feed_context(self):
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
    def test_create_post_GET(self):
        """create post get test"""
        request = self.factory.get(self.post_create_url)
        request.user = self.user1
        response = post_create.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_create_post_POST(self):
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
    def test_edit_post_GET(self):
        """update post get test"""
        request = self.factory.get(self.post_update_url)
        request.user = self.user1
        response = post_update.as_view()(request, pk=1)
        self.assertEquals(response.status_code, 200)

    def test_update_post_POST(self):
        """update post submit response code"""
        response = self.client.post(self.post_update_url, {
            'author': self.user1.username,
            'content': 'tests are very exciting'
        }, follow=True, pk=1)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, self.feed_url)

    # delete post
    def test_delete_post_GET(self):
        """update post get test"""
        request = self.factory.get(self.post_delete_url)
        request.user = self.user1
        response = post_delete.as_view()(request, pk=1)
        self.assertEquals(response.status_code, 200)
        
    def test_delete_post_POST(self):
        """delete post submit response code"""
        response = self.client.post(self.post_delete_url, follow=True, pk=1)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, self.feed_url)
        posts_by_user = Post.objects.filter(author=self.user1)
        # 1 from setUP and 0 after delete
        self.assertEquals(len(posts_by_user), 0)

    # post detail

    def test_post_detail_GET(self):
        """ post detail get response test"""
        request = self.factory.get(self.post_detail_url)
        request.user = self.user1
        response = post_detail.as_view()(request, pk=1)
        self.assertEquals(response.status_code, 200)
        

    def test_post_detail_POST(self):
        """ post detail POST data test"""
        response = self.client.post(self.post_detail_url, {
            'comment': 'test comment',
            'author': self.user2,
            'post': self.post1
        }, follow=True, pk=1)
        self.assertEquals(response.status_code, 200)
        comments = Comment.objects.filter(post=self.post1)
        # 1 from setUp 1 just ccreated
        self.assertEquals(len(comments), 2)

