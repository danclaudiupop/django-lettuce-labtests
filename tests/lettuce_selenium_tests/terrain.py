from django.core.management import call_command
from django.db import connection
from django.conf import settings

from lettuce import before, after, world
from selenium import webdriver


@before.all
def initial_setup():
    call_command('syncdb', interactive=False, verbosity=1)
    world.browser = webdriver.Firefox()

#@before.each_scenario
#def reset_data(scenario):
    ## Clean up django.
    #call_command('flush', interactive=False, verbosity=0)
    #call_command('loaddata', 'all', verbosity=0)

@after.all
def teardown_browser(total):
    connection.creation.destroy_test_db(settings.DATABASES['default']['NAME'])
    world.browser.quit()
