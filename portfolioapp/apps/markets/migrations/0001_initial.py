# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Market'
        db.create_table(u'markets_market', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('mic', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('acr', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'markets', ['Market'])


    def backwards(self, orm):
        # Deleting model 'Market'
        db.delete_table(u'markets_market')


    models = {
        u'markets.market': {
            'Meta': {'object_name': 'Market'},
            'acr': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mic': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        }
    }

    complete_apps = ['markets']