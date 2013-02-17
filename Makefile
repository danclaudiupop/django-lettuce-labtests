run-tests:

	@echo "Running lettuce tests"
	python manage.py harvest tests/lettuce_djangoclient_tests --settings=conf.settings
	python manage.py harvest tests/lettuce_selenium_tests --settings=conf.settings_lettuce
