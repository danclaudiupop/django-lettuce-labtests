import logging

from django.conf import settings
from django.core.management import call_command
from django.test import Client
from django.db import connection
#from django.test.utils import setup_test_enviroment, teardown_test_environment

from lettuce import *


@before.all
def initial_setup():
    logging.info("Loading django's test client ...\n")
    world.browser = Client()

    logging.info("Setting up a test database ...\n")

    try:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()
    except ImportError:
        pass

    # Setup test environment / called by harvest.py
    #setup_test_enviroment()

    world.testdb = connection.creation.create_test_db(
        verbosity=2,
        autoclobber=False,
    )


@after.all
def teardown_browser(total):
    logging.info("Destroy test database ...\n")
    connection.creation.destroy_test_db(world.testdb, verbosity=2)

    # Tear Down the test environment / called by harvest.py
    #teardown_test_enviroment()


@after.each_scenario
def before_each_feature(scenario):
    logging.info("Flusing db ... \n")

    call_command('flush', **{
        'settings': settings.SETTINGS_MODULE,
        'interactive': False,
        'verbosity': 1
    })
