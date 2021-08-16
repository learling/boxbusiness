from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def login_test_user(self):
        self.client.login(username='test-user', password='test-pass')

    def setUp(self):
        self.client = Client()
        self.login_path = reverse('login')
        self.login_response = self.client.get(self.login_path)
        self.profile_path = reverse('profile')
        self.logout_path = reverse('logout')

    def test_register_response_GET(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_login_response_GET(self):
        self.login_test_user()
        self.assertEquals(self.login_response.status_code, 200)
        self.assertTemplateUsed(self.login_response, 'accounts/login.html')

    def test_logout_response(self):
        self.login_test_user()
        response = self.client.get(self.logout_path)
        self.assertRedirects(response, self.login_path)

    def test_profile_response_GET(self):
        response = self.client.get(self.profile_path)
        expected_redirect = f'{self.login_path}?next={self.profile_path}'
        self.assertRedirects(response, expected_redirect)