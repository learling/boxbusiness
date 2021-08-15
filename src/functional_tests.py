from selenium import webdriver

def assert_success(browser):
    try:
        browser.get('http://localhost:8000')
        assert 'BoxBusiness' in browser.title
    finally:
        browser.quit()

assert_success(webdriver.Firefox())

assert_success(webdriver.Chrome())

# https://www.obeythetestinggoat.com/book/pre-requisite-installations.html
# Download and copy geckodriver to /usr/local/bin
# python3 manage.py runserver
# In another shell, run the automatic tests:
# python3 functional_tests.py
# No news is good news!
