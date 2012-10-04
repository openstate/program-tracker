# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Party.fullName'
        db.delete_column('core_party', 'fullName')

        # Adding field 'Party.full_name'
        db.add_column('core_party', 'full_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'Party.fullName'
        raise RuntimeError("Cannot reverse this migration. 'Party.fullName' and its values cannot be restored.")

        # Deleting field 'Party.full_name'
        db.delete_column('core_party', 'full_name')


    models = {
        'core.paragraph': {
            'Meta': {'ordering': "['order']", 'object_name': 'Paragraph'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paragraphs'", 'to': "orm['core.Section']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'core.party': {
            'Meta': {'object_name': 'Party'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pm_id': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.program': {
            'Meta': {'object_name': 'Program'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'programs'", 'to': "orm['core.Party']"}),
            'section': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'program_root'", 'unique': 'True', 'null': 'True', 'to': "orm['core.Section']"})
        },
        'core.section': {
            'Meta': {'ordering': "['order']", 'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subsections'", 'null': 'True', 'to': "orm['core.Section']"}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sections'", 'null': 'True', 'to': "orm['core.Program']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['core.SectionType']"})
        },
        'core.sectiontype': {
            'Meta': {'object_name': 'SectionType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['core']
