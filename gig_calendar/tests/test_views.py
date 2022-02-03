from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from gig_calendar.models import Event
from gig_calendar.views import(
    CalendarView,
    event_create,
    event_detail_view,
    event_update,
    event_delete,
)
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.calendar_url = reverse('cal:calendar')
        self.create_event_url = reverse('cal:event-create')
        self.event_detail_url = reverse('cal:event_detail', args=[1])
        self.event_update_url = reverse('cal:event-update', args=[1])
        self.event_delete_url = reverse('cal:event-delete', args=[1])
        self.factory = RequestFactory()
        self.user1 = User.objects.create(
            username = 'test',
            email = 'test@email.com',
            password = 'test12344321',
        )
        self.event = Event.objects.create(
            author = self.user1,
            title = 'title',
            description = 'test',
            date = '2022-01-01'
        )

    def test_calendar_view_GET(self):
        request = self.factory.get(self.calendar_url)
        request.user = self.user1
        response = CalendarView.as_view()(request)

        self.assertEquals(response.status_code, 200)

    def test_event_create_view_GET(self):
        request = self.factory.get(self.create_event_url)
        request.user = self.user1
        response = event_create.as_view()(request)

        self.assertEquals(response.status_code, 200)

    def test_event_detail_view_GET(self):
        request = self.factory.get(self.event_detail_url)
        request.user = self.user1
        response = event_detail_view.as_view()(request, pk=self.event.pk)
        self.assertEquals(response.status_code, 200)

    def test_event_update_view_GET(self):
        request = self.factory.get(self.event_update_url)
        request.user = self.user1
        response = event_update.as_view()(request, pk=self.event.pk)
        self.assertEquals(response.status_code, 200)

    def test_event_delete_view_GET(self):
        request = self.factory.get(self.event_delete_url)
        request.user = self.user1
        response = event_delete.as_view()(request, pk=self.event.pk)
        self.assertEquals(response.status_code, 200)

        
     


    

