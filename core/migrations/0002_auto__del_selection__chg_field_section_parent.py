# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Selection'
        db.delete_table('core_selection')

        # Changing field 'Section.parent'
        db.alter_column('core_section', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['core.Section']))


    def backwards(self, orm):
        
        # Adding model 'Selection'
        db.create_table('core_selection', (
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('startParagraph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.Paragraph'])),
            ('endLetter', self.gf('django.db.models.fields.IntegerField')()),
            ('startLetter', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('endParagraph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.Paragraph'])),
        ))
        db.send_create_signal('core', ['Selection'])

        # Changing field 'Section.parent'
        db.alter_column('core_section', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['core.Section']))


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
            'program': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': "orm['core.Program']"})
        }
    }

    complete_apps = ['core']
