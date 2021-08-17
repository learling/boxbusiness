from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import *


class TestPages(SimpleTestCase):

    def test_home_url_should_be_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_home_GET_should_show_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')