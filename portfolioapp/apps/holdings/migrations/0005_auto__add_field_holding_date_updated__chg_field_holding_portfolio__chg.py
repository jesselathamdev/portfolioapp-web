# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Holding.date_updated'
        db.add_column(u'holdings_holding', 'date_updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 1, 17, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'Holding.portfolio'
        db.alter_column(u'holdings_holding', 'portfolio_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['portfolios.Portfolio']))

        # Changing field 'Holding.date_created'
        db.alter_column(u'holdings_holding', 'date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Holding.market'
        db.alter_column(u'holdings_holding', 'market', self.gf('django.db.models.fields.CharField')(default='TSE', max_length=10))

    def backwards(self, orm):
        # Deleting field 'Holding.date_updated'
        db.delete_column(u'holdings_holding', 'date_updated')


        # Changing field 'Holding.portfolio'
        db.alter_column(u'holdings_holding', 'portfolio_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portfolios.Portfolio'], null=True))

        # Changing field 'Holding.date_created'
        db.alter_column(u'holdings_holding', 'date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Holding.market'
        db.alter_column(u'holdings_holding', 'market', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

    models = {
        u'holdings.holding': {
            'Meta': {'object_name': 'Holding'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'portfolio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portfolios.Portfolio']"}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'portfolios.portfolio': {
            'Meta': {'object_name': 'Portfolio'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['holdings']