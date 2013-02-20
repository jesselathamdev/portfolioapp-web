# settings/prod.py

import dj_database_url

from .base import *

DATABASES = {
    'default': { }
}

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

MIDDLEWARE_CLASSES += (
    'portfolioapp.apps.core.middleware.UserBasedExceptionMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = [
    'portfolioapp.conceptmob.com'
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
         'require_debug_false': {
             '()': 'django.utils.log.RequireDebugFalse',
         }
     },
    'handlers': {
        'console':{
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}