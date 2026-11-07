from django.test import SimpleTestCase
from django.urls import reverse

class LogoutViewTest(SimpleTestCase):
    def test_logout_redirect_home(self):
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(response, '/', fetch_redirect_response=False)