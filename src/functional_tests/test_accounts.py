from selenium.webdriver.common.keys import Keys
from .base import FunctionalTests
from django.urls import reverse

REGISTER_PATTERN = 'R(egister|EGISTER)'
LOGIN_PATTERN = 'L(ogin|OGIN)'


class TestAuthentication(FunctionalTests):

    def wait_for_open_page(self, path, expected_regex):
        self.browser.get(self.live_server_url + reverse(path))
        self.wait_for_body_contains(expected_regex)

    def login_invalid_user(self, username, password):
        self.register_valid_user()
        self.wait_for_body_contains(LOGIN_PATTERN)
        self.browser.find_element_by_name('username').send_keys(username)
        self.browser.find_element_by_name('password').send_keys(password)
        submit = "//input[@type='submit' and @value='Login']"
        self.browser.find_element_by_xpath(submit).click()
        self.wait_for_body_contains(LOGIN_PATTERN)
        or_ = ' [oO][rR] '
        name_or_passw = f'([uU]sername{or_}password)|([pP]assword{or_}[uU]sername)'
        name_or_passw + ' (is)? incorrect'
        self.wait_for_body_contains(name_or_passw + ' (is)? incorrect')

    def register_user(self, username, email, password1, password2):
        self.browser.find_element_by_name('username').send_keys(username)
        self.browser.find_element_by_name('email').send_keys(email)
        self.browser.find_element_by_name('password1').send_keys(password1)
        self.browser.find_element_by_name('password2').send_keys(password2)
        submit = "//input[@type='submit' and @value='Register']"
        self.browser.find_element_by_xpath(submit).click()

    def register_valid_user(self):
        self.wait_for_open_page('register', REGISTER_PATTERN)
        self.register_user(self.u['name'], self.u['email'], self.u['passw'], self.u['passw'])

    def test_login_valid_user(self):
        self.register_valid_user()
        self.wait_for_body_contains(LOGIN_PATTERN)
        self.browser.find_element_by_name('username').send_keys(self.u['name'])
        self.browser.find_element_by_name('password').send_keys(self.u['passw'])
        submit = "//input[@type='submit' and @value='Login']"
        self.browser.find_element_by_xpath(submit).click()
        self.wait_for_body_contains('Log out')

    def test_login_incorrect_username(self):
        self.login_invalid_user(self.u['name'], 'wrong' + self.u['passw'])

    def test_login_incorrect_password(self):
        self.login_invalid_user('wrong' + self.u['name'], self.u['passw'])

    def test_login_completely_wrong(self):
        self.login_invalid_user('wrong' + self.u['name'], 'wrong' + self.u['passw'])

    def test_register_mismatch_password_error(self):
        self.wait_for_open_page('register', 'Register')
        self.register_user(self.u['name'], self.u['email'], self.u['passw'], self.u['passw'] + '2')
        self.wait_for_body_contains(REGISTER_PATTERN)
        self.errorlist_contains('[pP]assword fields didn.t match')

    def test_register_existing_user_error(self):
        self.register_valid_user()
        self.wait_for_open_page('register', REGISTER_PATTERN)
        self.register_valid_user()
        self.wait_for_body_contains(REGISTER_PATTERN)
        self.errorlist_contains('[uU]sername (already)? exists')
