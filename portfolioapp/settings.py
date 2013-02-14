# Django settings for portfolioapp project.
from unipath import Path
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = Path(__file__).ancestor(2)

MEDIA_ROOT = PROJECT_ROOT.child('media')
STATIC_ROOT = PROJECT_ROOT.child('static')
STATICFILES_DIRS = (PROJECT_ROOT.child('assets'),)
TEMPLATE_DIRS = (PROJECT_ROOT.child('templates'),)

ADMINS = ('Jesse Latham', 'jesse.latham.dev@gmail.com')

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'portfolioapp',
        'USER': 'portfolioapp',
        'PASSWORD': 'access',
        'HOST': '',
        'PORT': '5432',
    }
}

# taken from: http://code.google.com/p/wadofstuff/wiki/DjangoFullSerializers; extends the existing json serializer with some extra goodness
SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Vancouver'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/assets/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'dajaxice.finders.DajaxiceFinder',
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
    'portfolioapp.apps.core.middleware.ProfilerMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

STATSD_PATCHES = [
    'django_statsd.patches.db',
    'django_statsd.patches.cache',
]

STATSD_CLIENT = 'django_statsd.clients.toolbar'

ROOT_URLCONF = 'portfolioapp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'portfolioapp.wsgi.application'

INSTALLED_APPS = (
    # django core apps
    #'django.contrib.admin',
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
    'portfolioapp.apps.core',
    'portfolioapp.apps.admin',

    # 3rd party addons
    'endless_pagination',
    'dajaxice',
    'dajax',

    # development tools
    'south',
    'django_extensions',
    'debug_toolbar',
    'django_statsd',
)

# Required for debug_toolbar
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    'django_statsd.panel.StatsdPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

AUTH_USER_MODEL = 'profiles.User'
AUTHENTICATION_BACKENDS = ('portfolioapp.apps.profiles.backends.Auth',)
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/sign-in'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}