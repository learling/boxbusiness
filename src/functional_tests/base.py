from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.conf import settings
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
import time

# https://github.com/hjwp/book-example/blob/chapter_fixtures_and_wait_decorator/functional_tests/base.py

MAX_WAIT = 9


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTests(StaticLiveServerTestCase):

    def delete_test_user(self):
        try:
            u = User.objects.get(username=self.u['name'])
            u.delete()
        except User.DoesNotExist:
            pass

    def setUp(self):
        self.u = settings.TEST_USER
        self.delete_test_user()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.browser.quit()
        self.delete_test_user()

    @wait
    def wait_for(self, fn):
        return fn()

    def wait_for_body_contains(self, expected_regex):
        self.wait_for(lambda:self.assertRegex(
            self.browser.find_element_by_tag_name('body').text,
            expected_regex
        ))

    def assert_errorlist_contains(self, expected_regex):
        self.assertRegex(
            self.browser.find_element_by_class_name('errorlist').text,
            expected_regex
        )
