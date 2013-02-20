# apps/middleware.py
# borrowed from http://djangosnippets.org/snippets/1579/

import cProfile
import sys
import os
import pstats
import tempfile
from cStringIO import StringIO

from django.conf import settings
from django.views.debug import technical_500_response

# the following is for profile
class ProfilerMiddleware(object):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG and 'prof' in request.GET:
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)

    def process_response(self, request, response):
        if settings.DEBUG and 'prof' in request.GET:
            (fd, self.profiler_file) = tempfile.mkstemp()
            self.profiler.dump_stats(self.profiler_file)
            out = StringIO()
            stats = pstats.Stats(self.profiler_file, stream=out)
            stats.strip_dirs()          # Must happen prior to sort_stats
            if request.GET['prof']:
                stats.sort_stats(request.GET['prof'])
            stats.print_stats()
            os.unlink(self.profiler_file)
            response.content = '<pre>%s</pre>' % out.getvalue()
        return response

class UserBasedExceptionMiddleware(object):
    """
    Borrowed from http://ericholscher.com/blog/2008/nov/15/debugging-django-production-environments/
    """
    def process_exception(self, request, exception):
        if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())