from django.test import TestCase, Client
from django.contrib.auth.models import User
from social.models import Musician
from social.forms import (
    UserSignUpForm,
    UserLoginForm,
    UserUpdateForm,
    UserPasswordResetForm,
    PasswordChangeForm,
)


class TestForms(TestCase):
    """test social app forms"""
    def setUp(self):
        """set up test variables"""
        self.client = Client()
        self.user1 = User.objects.create(
            username='test',
            email='test@email.com',
            password='test12344321',
        )

    def test_user_sign_up_valid_data(self):
        """test user sign up form w/ valid data"""
        form = UserSignUpForm(data={
            'username': 'test1',
            'email': 'test@email.com',
            'password1': 'test12344321',
            'password2': 'test12344321'
        })

        self.assertTrue(form.is_valid())

    def test_user_sign_up_not_valid_data(self):
        """test user sign up form w/ invalid data"""
        form = UserSignUpForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_user_login_valid_data(self):
        """test user login form w/ valid data"""
        form = UserLoginForm(data={
            'username': 'john',
            'password': 'smith'
            })
        self.assertTrue(form.is_valid)

    def test_user_login_not_valid_data(self):
        """test user login form w/ invalid data"""
        form = UserLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_user_update_valid_data(self):
        """test user update form w/ valid data"""
        form = UserUpdateForm(data={
            'first_name': 'john',
            'last_name': 'smith'
            })
        self.assertTrue(form.is_valid)

    def test_user_update_blank_is_not_valid_data(self):
        """test user update form w/ invalid data"""
        form = UserUpdateForm(data={})
        self.assertTrue(form.is_valid())

    def test_user_reset_valid_data(self):
        """test user update form w/ valid data on page reset"""
        form = UserPasswordResetForm(data={
            'email': 'john@mail.com',
            })
        self.assertTrue(form.is_valid)

    def test_user_reset_blank_is_not_valid_data(self):
        """test user update form w/ invalid data on page reset"""
        form = UserPasswordResetForm(data={})
        self.assertFalse(form.is_valid())

    def test_user_pass_reset_valid_data(self):
        """test user password reset form w/ valid data"""
        form = PasswordChangeForm(user=self.user1, data={
            'new_password1': 'test12344321',
            'new_password2': 'test12344321'
        })

        self.assertTrue(form.is_valid())

    def test_user_pass_reset_not_valid_data(self):
        """test user password reset form w/ invalid data"""
        form = PasswordChangeForm(user=self.user1, data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
