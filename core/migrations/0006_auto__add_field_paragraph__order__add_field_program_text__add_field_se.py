# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Paragraph._order'
        db.add_column('core_paragraph', '_order', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Program.text'
        db.add_column('core_program', 'text', self.gf('django.db.models.fields.related.OneToOneField')(related_name='program_root', unique=True, null=True, to=orm['core.Section']), keep_default=False)

        # Adding field 'Section._order'
        db.add_column('core_section', '_order', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Paragraph._order'
        db.delete_column('core_paragraph', '_order')

        # Deleting field 'Program.text'
        db.delete_column('core_program', 'text_id')

        # Deleting field 'Section._order'
        db.delete_column('core_section', '_order')


    models = {
        'core.paragraph': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Paragraph'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'programs'", 'to': "orm['core.Party']"}),
            'text': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'program_root'", 'unique': 'True', 'null': 'True', 'to': "orm['core.Section']"})
        },
        'core.section': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Section'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
        }
    }

    complete_apps = ['core']
