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
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_impressum_url_should_be_resolved(self):
        url = reverse('impressum')
        self.assertEquals(resolve(url).func, impressum)

    def test_impressum_GET_should_show_impressum_page(self):
        response = self.client.get(reverse('impressum'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/impressum.html')

    def test_datenschutz_url_should_be_resolved(self):
        url = reverse('datenschutz')
        self.assertEquals(resolve(url).func, datenschutz)

    def test_datenschutz_GET_should_show_datenschutz_page(self):
        response = self.client.get(reverse('datenschutz'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/datenschutz.html')