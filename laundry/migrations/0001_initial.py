# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hall'
        db.create_table('laundry_hall', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('location_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('laundry', ['Hall'])

        # Adding model 'LaundryMachine'
        db.create_table('laundry_laundrymachine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('type', self.gf('django.db.models.fields.TextField')()),
            ('hall', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['laundry.Hall'])),
        ))
        db.send_create_signal('laundry', ['LaundryMachine'])

        # Adding model 'LaundryRecord'
        db.create_table('laundry_laundryrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='records', to=orm['laundry.LaundryMachine'])),
            ('availability', self.gf('django.db.models.fields.TextField')()),
            ('time_remaining', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('laundry', ['LaundryRecord'])


    def backwards(self, orm):
        # Deleting model 'Hall'
        db.delete_table('laundry_hall')

        # Deleting model 'LaundryMachine'
        db.delete_table('laundry_laundrymachine')

        # Deleting model 'LaundryRecord'
        db.delete_table('laundry_laundryrecord')


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