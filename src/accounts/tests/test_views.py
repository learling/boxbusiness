from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.messages import get_messages


class TestViews(TestCase):

    def setUp(self):
        self.u = settings.TEST_USER
        self.client = Client()

    def tearDown(self):
        try:
            u = User.objects.get(username=self.u['name'])
            u.delete()
        except User.DoesNotExist:
            pass

    def register_test_user(self):
        return self.client.post(reverse('register'), {
            'username': self.u['name'],
            'email': self.u['email'],
            'password1': self.u['passw'],
            'password2': self.u['passw']
        })

    def assert_no_creation(self, response):
        u = User.objects.filter(username=self.u['name']).all()
        self.assertLessEqual(len(u), 1)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_POST_valid_input_should_create_customer(self):
        response = self.register_test_user()
        user = User.objects.last()
        self.assertEquals(user.username, self.u['name'])
        group = Group.objects.get(name='customer')
        self.assertEquals(len(user.groups.all()), 1)
        self.assertEquals(user.groups.all()[0], group)

    def test_register_POST_valid_input_should_show_login_page(self):
        response = self.register_test_user()
        self.assertRedirects(response, reverse('login'))

    def test_register_POST_duplicate_should_not_create_twice(self):
        response = self.register_test_user()
        response = self.register_test_user()
        self.assert_no_creation(response)

    def test_register_POST_empty_input_should_not_register(self):
        response = self.client.post(reverse('register'), {
            'username': '',
            'email': '',
            'password1': '',
            'password2': ''
        })
        self.assert_no_creation(response)

    def test_login_POST_valid_input_should_login_user(self):
        self.register_test_user()
        response = self.client.post(reverse('login'), {
            'username': self.u['name'],
            'password': self.u['passw']
        })
        self.assertTrue(
            '_auth_user_id' in self.client.session
        )

    def test_login_POST_invalid_input_should_not_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'badboy',
            'password': 'wr0ngPa8w'
        })
        self.assertFalse(
            '_auth_user_id' in self.client.session
        )

    def test_login_POST_invalid_input_should_show_message(self):
        response = self.client.post(reverse('login'), {
            'username': 'badboy',
            'password': 'wr0ngPa8w'
        })
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(len(messages), 1)
        self.assertIn('incorrect', messages[0])

    def test_login_POST_empty_input_should_not_login(self):
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': ''
        })
        self.assertFalse(
            '_auth_user_id' in self.client.session
        )