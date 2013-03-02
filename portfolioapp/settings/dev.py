    # settings/local.py

from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

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

MIDDLEWARE_CLASSES += (
  'portfolioapp.apps.core.middleware.ProfilerMiddleware',
  'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    # development tools
    'django_extensions',
    'debug_toolbar',
    'devserver',
)

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
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

TEMPLATE_STRING_IF_INVALID = 'INVALID EXPRESSION: %s'