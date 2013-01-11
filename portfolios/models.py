from django.db import models

class Portfolio(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name