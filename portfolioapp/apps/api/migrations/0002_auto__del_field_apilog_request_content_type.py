# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ApiLog.request_content_type'
        db.delete_column('api_logs', 'request_content_type')


    def backwards(self, orm):
        # Adding field 'ApiLog.request_content_type'
        db.add_column('api_logs', 'request_content_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, null=True, blank=True),
                      keep_default=False)


    models = {
        u'api.apilog': {
            'Meta': {'object_name': 'ApiLog', 'db_table': "'api_logs'"},
            'api_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'null': 'True'}),
            'api_version': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_body': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'request_http_user_agent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'request_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'request_ip_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'request_method': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'request_path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'request_query_string': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'response_status_code': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['api']