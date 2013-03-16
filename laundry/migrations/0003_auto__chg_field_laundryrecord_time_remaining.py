# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'LaundryRecord.time_remaining'
        db.alter_column('laundry_laundryrecord', 'time_remaining', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'LaundryRecord.time_remaining'
        db.alter_column('laundry_laundryrecord', 'time_remaining', self.gf('django.db.models.fields.IntegerField')(default=0))

    models = {
        'laundry.hall': {
            'Meta': {'object_name': 'Hall'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_id': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        'laundry.laundrymachine': {
            'Meta': {'object_name': 'LaundryMachine'},
            'hall': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['laundry.Hall']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'type': ('django.db.models.fields.TextField', [], {})
        },
        'laundry.laundryrecord': {
            'Meta': {'object_name': 'LaundryRecord'},
            'availability': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'records'", 'to': "orm['laundry.LaundryMachine']"}),
            'time_remaining': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['laundry']