from model_bakery import baker
from accounts.models import CustomUser
from django.test import TestCase
from unittest import mock

DEFAULT_IMAGE = 'profiles/default_profile.png'

class TestCustomModel(TestCase):
    def setUp(self):
        self.user = baker.make(CustomUser, username='sam')

    def test_str(self):
        self.assertEqual(str(self.user), 'sam')

    def test_new_user_default_profile_image(self):
        self.assertEqual(self.user.profile_image.name, DEFAULT_IMAGE)

    def test_new_profile_image_on_changes(self):
        pass


    def test_old_profile_image_when_changed(self):
        pass
