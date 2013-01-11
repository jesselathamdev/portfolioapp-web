from django.db import models

class Holding(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name + " (" + self.symbol + ")"