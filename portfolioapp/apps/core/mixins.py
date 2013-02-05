# core/mixins.py

from django.db import models

class TimeStampMixin(models.Model):
    """
    Simple mixin to provide support for common dates in models
    """
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ORMMixin():
    def first(self):
        try:
            return self.all()[0]
        except:
            return None

    def last(self):
        try:
            items = self.all()
            return items[len(items)-1]
        except:
            return None