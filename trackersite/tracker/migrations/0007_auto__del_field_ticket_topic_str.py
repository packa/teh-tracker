# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Ticket.topic_str'
        db.delete_column('tracker_ticket', 'topic_str')


    def backwards(self, orm):
        
        # Adding field 'Ticket.topic_str'
        db.add_column('tracker_ticket', 'topic_str', self.gf('django.db.models.fields.CharField')(default='', max_length=80), keep_default=False)


    models = {
        'tracker.ticket': {
            'Meta': {'ordering': "['-updated']", 'object_name': 'Ticket'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requested_by': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Topic']", 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        'tracker.topic': {
            'Meta': {'ordering': "['name']", 'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'open_for_tickets': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['tracker']
