from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts import views
from django.contrib.auth.views import LogoutView

class TestUrls(SimpleTestCase):
    def test_sign_up(self):
        url = reverse('accounts:sign_up')
        self.assertEqual(resolve(url).func.view_class, views.SignUpView)

    def test_login(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.view_class, views.UserLoginView)

    def test_logout(self):
        url = reverse('accounts:logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_edit_profile(self):
        url = reverse('accounts:edit')
        self.assertEqual(resolve(url).func.view_class, views.UserEditView)

    def test_delete_image(self):
        url = reverse('accounts:delete_image', args=('1',))
        self.assertEqual(resolve(url).func, views.delete_image)