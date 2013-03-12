Install notes:
--------------
* When running with Django 1.6, Tasty-pie needs a couple of changes to its source files:  
  * __models.py__:  
    _Replace:_ user = models.OneToOneField(User, related_name='api_key')  
    _With:_ user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='api_key')  
  * __resources.py__:  
    _Replace:_ from django.conf.urls.defaults import patterns, url  
    _With:_ from django.conf.urls import patterns, url  