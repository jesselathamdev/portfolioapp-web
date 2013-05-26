# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StockPriceHistory'
        db.create_table('stock_price_history', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('stock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['markets.Stock'])),
            ('price_opening', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=6, decimal_places=2)),
            ('price_closing', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=6, decimal_places=2)),
            ('price_high', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=6, decimal_places=2)),
            ('price_low', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=6, decimal_places=2)),
            ('volume', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal(u'markets', ['StockPriceHistory'])

        # Adding field 'Stock.pe'
        db.add_column('stocks', 'pe',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=4),
                      keep_default=False)

        # Adding field 'Stock.eps'
        db.add_column('stocks', 'eps',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=4),
                      keep_default=False)

        # Adding field 'Stock.outstanding_shares'
        db.add_column('stocks', 'outstanding_shares',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'StockPriceHistory'
        db.delete_table('stock_price_history')

        # Deleting field 'Stock.pe'
        db.delete_column('stocks', 'pe')

        # Deleting field 'Stock.eps'
        db.delete_column('stocks', 'eps')

        # Deleting field 'Stock.outstanding_shares'
        db.delete_column('stocks', 'outstanding_shares')


    models = {
        u'markets.market': {
            'Meta': {'object_name': 'Market', 'db_table': "'markets'"},
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
            'Meta': {'object_name': 'Stock', 'db_table': "'stocks'"},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_price_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 26, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'eps': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['markets.Market']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'outstanding_shares': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'pe': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '4'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        u'markets.stockpricehistory': {
            'Meta': {'object_name': 'StockPriceHistory', 'db_table': "'stock_price_history'"},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price_closing': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            'price_high': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            'price_low': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            'price_opening': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['markets.Stock']"}),
            'volume': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['markets']