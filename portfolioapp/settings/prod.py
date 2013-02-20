# settings/prod.py

from .base import *

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
    'portfolioapp.apps.core.middleware.UserBasedExceptionMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = [
    'localhost'
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