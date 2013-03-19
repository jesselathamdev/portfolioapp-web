# api/models.py

import uuid

from django.db import models
from django.conf import settings

from portfolioapp.apps.core.mixins import TimeStampMixin


class ApiLog(TimeStampMixin, models.Model):
    request_id = models.CharField(max_length=32, null=False)
    request_ip_address = models.CharField(max_length=20, default='', blank=True, null=True)
    request_path = models.CharField(max_length=250, default='', blank=True, null=True)
    request_method = models.CharField(max_length=7, default='', blank=True, null=True)
    request_body = models.CharField(max_length=500, default='', blank=True, null=True)
    request_query_string = models.CharField(max_length=250, default='', blank=True, null=True)
    request_http_user_agent = models.CharField(max_length=150, default='', blank=True, null=True)
    response_status_code = models.SmallIntegerField()
    api_key = models.CharField(max_length=40, default='', null=True)
    api_version = models.CharField(max_length=5, null=True)

    class Meta:
        db_table = 'api_logs'

    def __unicode__(self):
        return 'Logging event originating from %s' % self.request_ip_address


class ApiToken(TimeStampMixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    token = models.CharField(max_length=32, default=uuid.uuid1().hex, null=False)
    identifier = models.CharField(max_length=50, default=uuid.uuid1().hex, null=False)
    date_expires = models.DateTimeField(null=True)

    class Meta:
        db_table = 'api_tokens'