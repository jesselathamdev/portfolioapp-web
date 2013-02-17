# settings/prod.py

import dj_database_url

from .base import *

DATABASES = {
    'default': { }
}

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()