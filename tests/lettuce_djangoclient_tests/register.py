import re

from bs4 import BeautifulSoup

from lettuce import step, world
from django.core import mail
from django.core.urlresolvers import reverse
from nose.tools import assert_equals

from django.contrib.auth.models import User


@step(u'I go to the register page')
def i_go_to_the_register_page(step):
    response = world.browser.get(reverse('registration_register'))
    assert_equals(response.status_code, 200)
    world.html = BeautifulSoup(response.content)


@step(u'I go to the login page')
def i_go_to_the_login_page(step):
    response = world.browser.get(reverse('auth_login'))
    assert_equals(response.status_code, 200)
    world.html = BeautifulSoup(response.content)


@step(u'When I fill register form with:')
def when_i_fill_in_user_data_with(step):
    for data in step.hashes:
        world.data = data
    assert_equals(len(world.html.select('form')), 1)
    assert_equals(len(world.html.find_all('input', 'required')), 4)


@step(u'And I submit the data')
def and_i_submit_the_data(step):
    world.response = world.browser.post(
        reverse('registration_register'),
        world.data,
        follow=True
    )
    assert_equals(
        User.objects.filter(username=world.data['username']).exists(), True
    )
    assert_equals(world.response.status_code, 200)


@step(u'I should see "(.*)"')
def i_should_see(step, expected_response):
    html = BeautifulSoup(world.response.content)
    expected_text = html.find('h1').get_text()
    assert_equals(expected_text, expected_response)


@step(u'And I should receive an email at "([^"]*)" with the subject "([^"]*)"')
def i_should_receive_email_with_subject(step, address, subject):
    assert_equals(mail.outbox[0].to[0], address)
    assert_equals(mail.outbox[0].subject, subject)


@step(u'And I activate the account')
def and_i_activate_the_account(step):
    activation_url = re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        mail.outbox[0].body
    )
    world.response = world.browser.get(activation_url[0], follow=True)
    assert_equals(world.response.status_code, 200)


@step(u'Given following users exist')
def given_following_users_exist(step):
    for user_hash in step.hashes:
        user_data = user_hash.copy()
        password = user_data.pop("password", None)
        user, created = User.objects.get_or_create(**user_data)
        user.set_password(password)
        user.save()


@step(u'And I login as user "([^"]*)"')
def and_i_login_as_user_group1(step, username):
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            username=username,
            password='test123',
        )
    assert_equals(len(world.html.select('form')), 1)
    assert_equals(len(world.html.find_all('input')), 3)
    world.response = world.browser.post(
        reverse('auth_login'),
        {'username': username, 'password': 'test123'},
        follow=True
    )
    assert_equals(world.response.status_code, 200)
