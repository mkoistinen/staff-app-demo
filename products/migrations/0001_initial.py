# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProductTranslation'
        db.create_table(u'products_product_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['products.Product'])),
        ))
        db.send_create_signal(u'products', ['ProductTranslation'])

        # Adding unique constraint on 'ProductTranslation', fields ['language_code', 'master']
        db.create_unique(u'products_product_translation', ['language_code', 'master_id'])

        # Adding model 'Product'
        db.create_table(u'products_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(default='', max_length=16)),
            ('description', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Placeholder'], null=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'products', ['Product'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProductTranslation', fields ['language_code', 'master']
        db.delete_unique(u'products_product_translation', ['language_code', 'master_id'])

        # Deleting model 'ProductTranslation'
        db.delete_table(u'products_product_translation')

        # Deleting model 'Product'
        db.delete_table(u'products_product')


    models = {
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'products.product': {
            'Meta': {'object_name': 'Product'},
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16'}),
            'description': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'})
        },
        u'products.producttranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'ProductTranslation', 'db_table': "u'products_product_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['products.Product']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'})
        }
    }

    complete_apps = ['products']