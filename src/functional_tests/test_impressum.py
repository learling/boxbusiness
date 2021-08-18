from .test_auth import TestAuthentication
from django.urls import reverse
from django.conf import settings


class TestImpressum(TestAuthentication):

    def test_impressum_should_contain_address(self):
        self.browser.get(self.live_server_url + reverse('impressum'))
        self.wait_for_body_contains(settings.SITE_OWNER['address'])