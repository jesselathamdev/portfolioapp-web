# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Portfolio'
        db.create_table('portfolios', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'portfolios', ['Portfolio'])

        # Adding model 'Holding'
        db.create_table('holdings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('portfolio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portfolios.Portfolio'])),
            ('stock', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['markets.Stock'])),
        ))
        db.send_create_signal(u'portfolios', ['Holding'])

        # Adding model 'Transaction'
        db.create_table('transactions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('holding', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portfolios.Holding'])),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=5)),
            ('value', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=7, decimal_places=2)),
            ('type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=5)),
            ('comment', self.gf('django.db.models.fields.CharField')(default='', max_length=250, null=True, blank=True)),
            ('commission', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=6, decimal_places=2)),
            ('date_transacted', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'portfolios', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Portfolio'
        db.delete_table('portfolios')

        # Deleting model 'Holding'
        db.delete_table('holdings')

        # Deleting model 'Transaction'
        db.delete_table('transactions')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'date_last_price_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 14, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['markets.Market']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        u'portfolios.activity': {
            'Meta': {'object_name': 'Activity', 'db_table': "'activities'", 'managed': 'False'},
            'acr': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'commission': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'date_transacted': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'portfolio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portfolios.Portfolio']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.User']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'})
        },
        u'portfolios.holding': {
            'Meta': {'object_name': 'Holding', 'db_table': "'holdings'"},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'portfolio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portfolios.Portfolio']"}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['markets.Stock']"})
        },
        u'portfolios.portfolio': {
            'Meta': {'object_name': 'Portfolio', 'db_table': "'portfolios'"},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.User']"})
        },
        u'portfolios.transaction': {
            'Meta': {'object_name': 'Transaction', 'db_table': "'transactions'"},
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'commission': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_transacted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'holding': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portfolios.Holding']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '5'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}),
            'value': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'})
        },
        u'profiles.user': {
            'Meta': {'object_name': 'User', 'db_table': "'users'"},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['portfolios']