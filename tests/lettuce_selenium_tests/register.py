import re

from lettuce import step, world
from lettuce.django import django_url
from lettuce.django import mail
from nose.tools import assert_equals

from django.core.urlresolvers import reverse

from selenium.webdriver.support.wait import WebDriverWait


@step(u'I go to the register page')
def i_go_to_the_register_page(step):
    world.response = world.browser.get(
        django_url(reverse('registration_register'))
    )


@step(u'I go to the login page')
def i_go_to_the_login_page(step):
    world.response = world.browser.get(
        django_url(reverse('auth_login'))
    )


@step(u'I fill in "(.*)" with "(.*)"')
def i_fill_in(step, field, value):
    world.browser.find_element_by_name(field).send_keys(value)


@step(u'I press "(.*)"')
def i_press(step, button_id):
    button = world.browser.find_element_by_id(button_id)
    button.click()


@step(u'I should see "(.*)"')
def i_should_see(step, expected_response):
    w = WebDriverWait(world.browser, 5)
    w.until(lambda driver: driver.find_element_by_tag_name('h1'))
    h1 = world.browser.find_element_by_tag_name('h1')
    assert_equals(h1.text, expected_response)


@step(u'And I should receive an email at "([^"]*)" with the subject "([^"]*)"')
def i_should_receive_email_with_subject(step, address, subject):
    message = mail.queue.get(True, timeout=5)
    world.email_body = message.body
    assert_equals(message.subject, subject)
    assert_equals(message.recipients(), [address])


@step(u'And I activate the account')
def and_i_activate_the_account(step):
    activation_url = re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        world.email_body
    )
    world.response = world.browser.get(activation_url)
