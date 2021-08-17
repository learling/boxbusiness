from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.messages import get_messages

class TestViews(TestCase):

    def login_test_user(self):
        user = User.objects.create(username=self.u['name'])
        user.set_password(self.u['passw'])
        user.save()
        self.client.login(username=self.u['name'], password=self.u['passw'])

    def create_test_user(self):
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

    def setUp(self):
        self.u = settings.TEST_USER
        self.client = Client()
        self.login_response = self.client.get(reverse('login'))

    def tearDown(self):
        try:
            u = User.objects.get(username=self.u['name'])
            u.delete()
        except User.DoesNotExist:
            pass

    def test_register_GET_anonymous_should_show_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_GET_authenticated_should_show_profile_page(self):
        self.login_test_user()
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('profile'))

    def test_login_GET_anonymous_should_show_login_page(self):
        self.assertEquals(self.login_response.status_code, 200)
        self.assertTemplateUsed(self.login_response, 'accounts/login.html')

    def test_login_GET_authenticated_should_show_profile_page(self):
        self.login_test_user()
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('profile'))
    
    def test_logout_GET_should_show_login_page(self):
        self.login_test_user()
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(
            '_auth_user_id' in self.client.session
        )

    def test_profile_GET_anonymous_should_show_login_page(self):
        response = self.client.get(reverse('profile'))
        expected_redirect = f'{reverse("login")}?next={reverse("profile")}'
        self.assertRedirects(response, expected_redirect)

    def test_profile_GET_authenticated_should_show_profile_page(self):
        self.login_test_user()
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_register_POST_valid_should_create_customer(self):
        response = self.create_test_user()
        user = User.objects.last()
        self.assertEquals(user.username, self.u['name'])
        group = Group.objects.get(name='customer')
        self.assertEquals(len(user.groups.all()), 1)
        self.assertEquals(user.groups.all()[0], group)

    def test_register_POST_valid_should_show_login_page(self):
        response = self.create_test_user()
        self.assertRedirects(response, reverse('login'))

    def test_register_POST_duplicate_should_not_register_twice(self):
        response = self.create_test_user()
        response = self.create_test_user()
        self.assert_no_creation(response)

    def test_register_POST_empty_should_not_register(self):
        response = self.client.post(reverse('register'), {
            'username': '',
            'email': '',
            'password1': '',
            'password2': ''
        })
        self.assert_no_creation(response)

    def test_register_POST_none_should_not_register(self):
        response = self.client.post(reverse('register'), {})
        self.assert_no_creation(response)

    def test_login_POST_valid_should_login_user(self):
        self.create_test_user()
        response = self.client.post(reverse('login'), {
            'username': self.u['name'],
            'password': self.u['passw']
        })
        self.assertTrue(
            '_auth_user_id' in self.client.session
        )

    def test_login_POST_invalid_credentials_should_not_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'badboy',
            'password': 'wr0ngPa8w'
        })
        self.assertFalse(
            '_auth_user_id' in self.client.session
        )

    def test_login_POST_invalid_credentials_should_show_message(self):
        response = self.client.post(reverse('login'), {
            'username': 'badboy',
            'password': 'wr0ngPa8w'
        })
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(len(messages), 1)
        self.assertIn('incorrect', messages[0])

    def test_login_POST_empty_should_not_login(self):
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': ''
        })
        self.assertFalse(
            '_auth_user_id' in self.client.session
        )