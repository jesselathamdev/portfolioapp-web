# settings/base.py

import os
from unipath import Path
from django.core.exceptions import ImproperlyConfigured
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

def get_env_variable(var_name):
    """ Get the environment variable name or return an exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the %s env variable' % var_name
        raise ImproperlyConfigured(error_msg)


PROJECT_ROOT = Path(__file__).ancestor(3)

MEDIA_ROOT = PROJECT_ROOT.child('media')
STATIC_ROOT = PROJECT_ROOT.child('static')
STATICFILES_DIRS = (PROJECT_ROOT.child('assets'),)
TEMPLATE_DIRS = (PROJECT_ROOT.child('templates'),)

ADMINS = ('Jesse Latham', 'jesse.latham.dev@gmail.com')

MANAGERS = ADMINS

# taken from: http://code.google.com/p/wadofstuff/wiki/DjangoFullSerializers; extends the existing json serializer with some extra goodness
SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

TIME_ZONE = 'America/Vancouver'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'portfolioapp.apps.core.context_processors.global_login_form',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9pl-a5047^pp6md04t!2a5r8a6(bh%@)oxc5jc370ty-w*(*23'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'portfolioapp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'portfolioapp.wsgi.application'

INSTALLED_APPS = (
    # django core apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',

    # portfolioapp specific
    'portfolioapp.apps.profiles',
    'portfolioapp.apps.portfolios',
    'portfolioapp.apps.markets',
    'portfolioapp.apps.cash',
    'portfolioapp.apps.core',
    'portfolioapp.apps.admin',

    # 3rd party addons
    'endless_pagination',
    'south',
)

AUTH_USER_MODEL = 'profiles.User'
AUTHENTICATION_BACKENDS = ('portfolioapp.apps.profiles.backends.Auth',)
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/sign-in'