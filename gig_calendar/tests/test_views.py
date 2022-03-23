from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from gig_calendar.models import Event
from organiser.models import Friend
from gig_calendar.views import(
    CalendarView,
    event_create,
    event_detail_view,
    event_update,
    event_delete,
    event_list_view,
    event_share,
    event_share_confirm,
    event_invite,
)


class TestViews(TestCase):
    """ test gig_calendar views """

    def setUp(self):
        """ set up test variables """
        self.client = Client()
        self.user1 = User.objects.create(
            username = 'test',
            email = 'test@email.com',
            password = 'test12344321',
        )
        self.user2 = User.objects.create(
            username = 'test2',
            email = 'test2@email.com',
            password = 'test12344321',
        )
        self.event = Event.objects.create(
            author = self.user1,
            title = 'title',
            description = 'test',
            date = '2022-01-01'
        )
        Friend.make_friend(self.user1, self.user2)
        self.client.force_login(self.user1)

        self.calendar_url = reverse('cal:calendar')
        self.create_event_url = reverse('cal:event-create')
        self.event_detail_url = reverse('cal:event_detail', args=[1])
        self.event_update_url = reverse('cal:event-update', args=[1])
        self.event_delete_url = reverse('cal:event-delete', args=[1])
        self.event_list_url = reverse('cal:event-list', kwargs={'slug_year': 2022, 'slug_month':1, 'slug_day': 1})
        self.event_share_url = reverse('cal:event_share', args=[1])
        self.event_share_confirm_url = reverse('cal:event_share_confirm', kwargs={'event_pk': self.event.pk, 'user_pk': self.user1.pk})
        self.event_invite_url = reverse('cal:event_invite', args=[1])
        self.factory = RequestFactory()
       
      
    def test_calendar_view_GET(self):
        """test calendar view results in 200 status code"""
        request = self.factory.get(self.calendar_url)
        request.user = self.user1
        response = CalendarView.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_event_create_view_GET(self):
        """test calendar event create results in 200 status code"""
        request = self.factory.get(self.create_event_url)
        request.user = self.user1
        response = event_create.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_create_event_post(self):
        """ test create a new event post """
        response = self.client.post(self.create_event_url, {
            'author': self.user1,
            'title': 'test2',
            'description':'test description',
            'date': '2022-01-01'}, pk=self.event.pk, follow=True)
        self.assertEquals(response.status_code, 200)
        # 1 from setup and 1 just created
        self.assertEquals(Event.objects.filter(author=self.user1).count(), 2)

    def test_event_detail_view_GET(self):
        """test calendar event detail results in 200 status code"""
        request = self.factory.get(self.event_detail_url)
        request.user = self.user1
        response = event_detail_view.as_view()(request, pk=self.event.pk)
        self.assertEquals(response.status_code, 200)

    def test_event_update_view_GET(self):
        """test calendar event update results in 200 status code"""
        request = self.factory.get(self.event_update_url)
        request.user = self.user1
        response = event_update.as_view()(request, pk=self.event.pk)
        self.assertEquals(response.status_code, 200)

    def test_event_update_post(self):
        """ test update event post """
        response = self.client.post(self.event_update_url, {
            'author': self.user1,
            'title': 'updated title',
            'description':'test description',
            'date': '2022-01-01'}, pk=self.event.pk, follow=True)
        self.assertEquals(response.status_code, 200)
        # check title has been updated
        self.assertEquals(Event.objects.get(pk=self.event.pk).title, 'updated title')

    def test_event_delete_view_GET(self):
        """test calendar event delete results in 200 status code"""
        request = self.factory.get(self.event_delete_url)
        request.user = self.user1
        response = event_delete.as_view()(request, pk=self.event.pk)
        self.assertEquals(response.status_code, 200)

    def test_event_list_view_GET(self):
        """test calendar event list results in 200 status code"""
        response = self.client.get(self.event_list_url)
        self.assertEquals(response.status_code, 200)

    def test_event_share_view_GET(self):
        """test calendar event share results in 200 status code"""
        request = self.factory.get(self.event_share_url)
        request.user = self.user1
        response = event_share.as_view()(request, pk=self.event.pk)
        self.assertEquals(response.status_code, 200)

    def test_event_share_confirm_view_POST(self):
        """test calendar event share confirm post results in 200 status code"""
        response = self.client.post(self.event_share_confirm_url, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_event_invite_view_GET(self):
        """test calendar event invite results in 200 status code"""
        request = self.factory.get(self.event_invite_url)
        request.user = self.user1
        response = event_invite.as_view()(request, pk=self.event.pk)
        self.assertEquals(response.status_code, 200)

    def test_event_invite_post(self):
        """ test event invite post """
        self.client.force_login(self.user2)
        response = self.client.post(self.event_invite_url, {
            'author': self.user2,
            'title': self.event.title,
            'description':self.event.description,
            'date': self.event.date}, pk=self.event.pk, follow=True)
        self.assertEquals(response.status_code, 200)
        # 1 from setup and 1 just saved
        self.assertEquals(Event.objects.all().count(), 2)
