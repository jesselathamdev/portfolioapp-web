# settings/test.py

from .base import *


########## DATABASE SETTINGS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'portfolioapp',
        'USER': 'portfolioapp',
        'PASSWORD': 'access',
        'HOST': '',
        'PORT': '5432',
        'TEST_NAME': 'portfolioapp_test',
    }
}


########## INSTALLED APPS REQUIRED FOR TESTING ENVIRONMENT
INSTALLED_APPS += (
    'django_nose',
)


########## TEST SETTINGS
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_TESTS_MIGRATE = True