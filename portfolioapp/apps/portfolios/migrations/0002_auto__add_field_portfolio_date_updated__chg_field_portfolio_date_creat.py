# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Portfolio.date_updated'
        db.add_column(u'portfolios_portfolio', 'date_updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 1, 17, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'Portfolio.date_created'
        db.alter_column(u'portfolios_portfolio', 'date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):
        # Deleting field 'Portfolio.date_updated'
        db.delete_column(u'portfolios_portfolio', 'date_updated')


        # Changing field 'Portfolio.date_created'
        db.alter_column(u'portfolios_portfolio', 'date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    models = {
        u'portfolios.portfolio': {
            'Meta': {'object_name': 'Portfolio'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['portfolios']