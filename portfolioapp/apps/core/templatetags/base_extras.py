# core/templatetags/base_extras.py

# borrowed from http://www.turnkeylinux.org/blog/django-navbar, see comments regarding resolve vs reverse for parameterized urls

from django import template
from django.core.urlresolvers import resolve, Resolver404

register = template.Library()

@register.simple_tag
def navactive(request, urls):
    try:
        url = resolve(request.path).url_name
        if url in urls:
            return 'active'
        else:
            return ''
    except Resolver404:
        return ''