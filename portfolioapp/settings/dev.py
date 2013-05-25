# settings/dev.py

from .base import *


########## MISC CONFIGURATION

DEBUG = True
TEMPLATE_DEBUG = DEBUG
TEMPLATE_STRING_IF_INVALID = 'INVALID EXPRESSION: %s'


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


########## INSTALLED APPS

INSTALLED_APPS += (
    # development tools
    'django_extensions',
    'debug_toolbar',
    'devserver',

    # testing tools
    'django_nose',
)


########## MIDDLEWARE

MIDDLEWARE_CLASSES += (
  'debug_toolbar.middleware.DebugToolbarMiddleware',
)


########## DEVSERVER MODULES AND CONFIGURATION

DEVSERVER_MODULES = (
    'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',
    'devserver.modules.ajax.AjaxDumpModule',
    'devserver.modules.cache.CacheSummaryModule',
    'devserver.modules.request.RequestDumpModule',
    'devserver.modules.request.ResponseDumpModule',
    # 'devserver.modules.request.SessionInfoModule', <- doesn't support django 1.5 custom user models yet, error on 'username'
)

DEVSERVER_TRUNCATE_SQL = False
DEVSERVER_ARGS = ['--werkzeug']


########## DEBUG TOOLBAR CONFIGURATION

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
)

INTERNAL_IPS = ('127.0.0.1',)  # Required for debug_toolbar

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}


########## TEST SETTINGS
# currently an issue exists here when running ./manage.py test, "conflicting option strings between core Django and django-nose I suspect - 2013-05-22

TEST_RUNNER = 'django_nose.BasicNoseRunner'
SOUTH_TESTS_MIGRATE = True