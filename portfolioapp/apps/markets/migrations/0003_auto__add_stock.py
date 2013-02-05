# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stock'
        db.create_table(u'markets_stock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('last_price', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=6, decimal_places=2)),
            ('market', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['markets.Market'])),
        ))
        db.send_create_signal(u'markets', ['Stock'])


    def backwards(self, orm):
        # Deleting model 'Stock'
        db.delete_table(u'markets_stock')


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
            'mic': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        u'markets.stock': {
            'Meta': {'object_name': 'Stock'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['markets.Market']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['markets']