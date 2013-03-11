Install notes:
- When running with Django 1.6, Tasty-pie needs a couple of changes to its source files:
    models.py:
        Replace: user = models.OneToOneField(User, related_name='api_key')
        With:    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='api_key')
    resources.py:
        Replace: from django.conf.urls.defaults import patterns, url
        With:    from django.conf.urls import patterns, url