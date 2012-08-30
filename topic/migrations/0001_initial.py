# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Topic'
        db.create_table('topic_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('creationdate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('topic', ['Topic'])

        # Adding model 'Selection'
        db.create_table('topic_selection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paragraph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='selections', to=orm['core.Paragraph'])),
            ('startLetter', self.gf('django.db.models.fields.IntegerField')()),
            ('endLetter', self.gf('django.db.models.fields.IntegerField')()),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='selections', to=orm['topic.Topic'])),
            ('creationdate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('topic', ['Selection'])


    def backwards(self, orm):
        
        # Deleting model 'Topic'
        db.delete_table('topic_topic')

        # Deleting model 'Selection'
        db.delete_table('topic_selection')


    models = {
        'core.paragraph': {
            'Meta': {'object_name': 'Paragraph'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paragraphs'", 'to': "orm['core.Section']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'core.party': {
            'Meta': {'object_name': 'Party'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.program': {
            'Meta': {'object_name': 'Program'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'programs'", 'to': "orm['core.Party']"})
        },
        'core.section': {
            'Meta': {'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subsections'", 'null': 'True', 'to': "orm['core.Section']"}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sections'", 'null': 'True', 'to': "orm['core.Program']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['core.SectionType']"})
        },
        'core.sectiontype': {
            'Meta': {'object_name': 'SectionType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'topic.selection': {
            'Meta': {'object_name': 'Selection'},
            'creationdate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'endLetter': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paragraph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'selections'", 'to': "orm['core.Paragraph']"}),
            'startLetter': ('django.db.models.fields.IntegerField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'selections'", 'to': "orm['topic.Topic']"})
        },
        'topic.topic': {
            'Meta': {'object_name': 'Topic'},
            'creationdate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['topic']
