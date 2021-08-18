from django.contrib.auth.models import User, Group
from django.urls import reverse
from .test_views import TestViews


class TestDecorators(TestViews):

    def login_test_user(self):
        self.user = User.objects.create(username=self.u['name'])
        self.user.set_password(self.u['passw'])
        self.user.save()
        self.client.login(username=self.u['name'], password=self.u['passw'])

    def test_register_GET_as_anonymous_should_show_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_GET_as_authenticated_should_show_profile_page(self):
        self.login_test_user()
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('profile'))

    def test_login_GET_as_anonymous_should_show_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_GET_as_authenticated_should_show_profile_page(self):
        self.login_test_user()
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('profile'))

    def test_logout_GET_should_show_login_page(self):
        self.login_test_user()
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_profile_GET_as_anonymous_should_require_login(self):
        response = self.client.get(reverse('profile'))
        expected_redirect = f'{reverse("login")}?next={reverse("profile")}'
        self.assertRedirects(response, expected_redirect)

    def test_profile_GET_as_authenticated_should_show_profile_page(self):
        self.login_test_user()
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_users_GET_as_customer_only_should_respond_unauthorized(self):
        self.login_test_user()
        response = self.client.get(reverse('users'))
        self.assertEquals(response.status_code, 401)

    def test_users_GET_as_admin_should_show_users(self):
        self.login_test_user()
        self.user.groups.add(Group.objects.get(name='admin'))
        response = self.client.get(reverse('users'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/users.html')