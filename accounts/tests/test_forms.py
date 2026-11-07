from django.test import TestCase
from accounts.forms import SignUpForm
from model_bakery import baker
from accounts.models import CustomUser

class TestSignUpForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        baker.make(CustomUser, username='kev345')

    def test_validate_data(self):
        form = SignUpForm(
            data={
                'first_name': 'kevin',
                'last_name': 'kev',
                'username': 'kev123',
                'email': 'kevin123@gmail.com',
                'password1': '123fffggg@',
                'password2': '123fffggg@'
            }
        )
        self.assertTrue(form.is_valid())

    def test_unmatched_password(self):
        form = SignUpForm(
            data={
                'first_name': 'kevin',
                'last_name': 'kev',
                'username': 'kev123',
                'email': 'kevin123@gmail.com',
                'password1': '123fffggg',
                'password2': '123fffggg@'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)

    def test_empty_data(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)
        self.assertTrue(form.has_error)

    def test_exists_email(self):
        form = SignUpForm(
            data={
                'first_name': 'kevin',
                'last_name': 'kev',
                'username': 'kev345',
                'email': 'kevin123@gmail.com',
                'password1': '123fffggg@',
                'password2': '123fffggg@'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('username'))


