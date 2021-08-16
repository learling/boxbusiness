from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.conf import settings

class TestViews(TestCase):

    def login_test_user(self):
        self.client.login(username='test-user', password='test-pass')

    def setUp(self):
        self.u = settings.TEST_USER
        self.client = Client()
        self.login_path = reverse('login')
        self.login_response = self.client.get(self.login_path)
        self.profile_path = reverse('profile')
        self.logout_path = reverse('logout')

    def test_register_GET(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_login_GET(self):
        self.login_test_user()
        self.assertEquals(self.login_response.status_code, 200)
        self.assertTemplateUsed(self.login_response, 'accounts/login.html')

    def test_logout_GET(self):
        self.login_test_user()
        response = self.client.get(self.logout_path)
        self.assertRedirects(response, self.login_path)

    def test_profile_GET(self):
        response = self.client.get(self.profile_path)
        expected_redirect = f'{self.login_path}?next={self.profile_path}'
        self.assertRedirects(response, expected_redirect)

    def test_register_POST_valid(self):
        response = self.client.post(reverse('register'), {
            'username': self.u['name'],
            'email': self.u['email'],
            'password1': self.u['passw'],
            'password2': self.u['passw']
        })
        user = User.objects.last();
        self.assertEquals(user.username, self.u['name'])
        group = Group.objects.get(name='customer')
        self.assertEquals(len(user.groups.all()), 1)
        self.assertEquals(user.groups.all()[0], group)
        self.assertRedirects(response, self.login_path)

    # TODO
    def test_register_POST_invalid(self):
        pass

    # TODO
    def test_register_POST_empty(self):
        pass

    # TODO
    def test_login_POST_valid(self):
        pass

    # TODO
    def test_login_POST_invalid(self):
        pass

    # TODO
    def test_login_POST_empty(self):
        pass