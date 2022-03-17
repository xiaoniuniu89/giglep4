from django.test import SimpleTestCase
from django.urls import reverse, resolve
from gig_calendar.views import (
    CalendarView,
    event_create,
    event_delete,
    event_detail_view,
    event_update,
    event_list_view,
    event_share,
    event_share_confirm,
    event_invite,
)


class TestUrls(SimpleTestCase):
    """test gig_calendar app urls"""

    def test_calendar_url_is_resolved(self):
        """test calendar url resolves"""
        url = reverse('cal:calendar')
        self.assertEquals(resolve(url).func.view_class, CalendarView)

    def test_event_create_url_is_resolved(self):
        """test event create url resolves"""
        url = reverse('cal:event-create')
        self.assertEquals(resolve(url).func.view_class, event_create)

    def test_event_delete_url_is_resolved(self):
        """test event delete url resolves"""
        url = reverse('cal:event-delete', args=[1234])
        self.assertEquals(resolve(url).func.view_class, event_delete)

    def test_event_detail_url_is_resolved(self):
        """test event detail url resolves"""
        url = reverse('cal:event_detail', args=[1234])
        self.assertEquals(resolve(url).func.view_class, event_detail_view)

    def test_event_update_url_is_resolved(self):
        """test event update url resolves"""
        url = reverse('cal:event-update', args=[1234])
        self.assertEquals(resolve(url).func.view_class, event_update)

    def test_event_share_list_url_is_resolved(self):
        """test event share list url resolves"""
        url = reverse(
            'cal:event-list',
            kwargs={'slug_year': 2022, 'slug_month': 1, 'slug_day': 1}
        )
        self.assertEquals(resolve(url).func.view_class, event_list_view)

    def test_event_share_url_is_resolved(self):
        """test event share url resolves"""
        url = reverse('cal:event_share', args=[1234])
        self.assertEquals(resolve(url).func.view_class, event_share)

    def test_event_share_confirm_url_is_resolved(self):
        """test event share confirm url resolves"""
        url = reverse(
            'cal:event_share_confirm',
            kwargs={'event_pk': 1, 'user_pk': 1}
        )
        self.assertEquals(resolve(url).func.view_class, event_share_confirm)

    def test_event_invite_url_is_resolved(self):
        """test event invite url resolves"""
        url = reverse('cal:event_invite', args=[1234])
        self.assertEquals(resolve(url).func.view_class, event_invite)
