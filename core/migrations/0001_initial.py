# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Party'
        db.create_table('core_party', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['Party'])

        # Adding model 'Program'
        db.create_table('core_program', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Party'])),
        ))
        db.send_create_signal('core', ['Program'])

        # Adding model 'Section'
        db.create_table('core_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('program', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Program'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Section'])),
        ))
        db.send_create_signal('core', ['Section'])

        # Adding model 'Paragraph'
        db.create_table('core_paragraph', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Section'])),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('core', ['Paragraph'])

        # Adding model 'Selection'
        db.create_table('core_selection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('startParagraph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.Paragraph'])),
            ('startLetter', self.gf('django.db.models.fields.IntegerField')()),
            ('endParagraph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.Paragraph'])),
            ('endLetter', self.gf('django.db.models.fields.IntegerField')()),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['Selection'])


    def backwards(self, orm):
        
        # Deleting model 'Party'
        db.delete_table('core_party')

        # Deleting model 'Program'
        db.delete_table('core_program')

        # Deleting model 'Section'
        db.delete_table('core_section')

        # Deleting model 'Paragraph'
        db.delete_table('core_paragraph')

        # Deleting model 'Selection'
        db.delete_table('core_selection')


    models = {
        'core.paragraph': {
            'Meta': {'object_name': 'Paragraph'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Section']"}),
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
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Party']"})
        },
        'core.section': {
            'Meta': {'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Section']"}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Program']"})
        },
        'core.selection': {
            'Meta': {'object_name': 'Selection'},
            'endLetter': ('django.db.models.fields.IntegerField', [], {}),
            'endParagraph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.Paragraph']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'startLetter': ('django.db.models.fields.IntegerField', [], {}),
            'startParagraph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.Paragraph']"})
        }
    }

    complete_apps = ['core']
