from django.test import SimpleTestCase
from django.urls import reverse, resolve
from gig_calendar.views import (CalendarView,
event_create,
event_delete,
event_detail_view,
event_update,
)

class TestUrls(SimpleTestCase):


    def test_calendar_url_is_resolved(self):
        url = reverse('cal:calendar')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, CalendarView)

    def test_event_create_url_is_resolved(self):
        url = reverse('cal:event-create')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, event_create)

    def test_event_delete_url_is_resolved(self):
        url = reverse('cal:event-delete', args=[1234])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, event_delete)

    def test_event_detail_url_is_resolved(self):
        url = reverse('cal:event_detail', args=[1234])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, event_detail_view)

    def test_event_update_url_is_resolved(self):
        url = reverse('cal:event-update', args=[1234])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, event_update)
        