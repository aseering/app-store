# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AppInstance'
        db.create_table('app_collection_appinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_collection.App'])),
            ('api_version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_collection.ApiVersion'])),
            ('setup_sql', self.gf('django.db.models.fields.TextField')()),
            ('remove_sql', self.gf('django.db.models.fields.TextField')()),
            ('so_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('app_collection', ['AppInstance'])

        # Adding model 'ApiVersion'
        db.create_table('app_collection_apiversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brand_version', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('sdk_version', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('app_collection', ['ApiVersion'])

        # Deleting field 'App.app'
        db.delete_column('app_collection_app', 'app')

        # Deleting field 'App.remove_sql'
        db.delete_column('app_collection_app', 'remove_sql')

        # Deleting field 'App.setup_sql'
        db.delete_column('app_collection_app', 'setup_sql')


    def backwards(self, orm):
        # Deleting model 'AppInstance'
        db.delete_table('app_collection_appinstance')

        # Deleting model 'ApiVersion'
        db.delete_table('app_collection_apiversion')

        # Adding field 'App.app'
        db.add_column('app_collection_app', 'app',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'App.remove_sql'
        db.add_column('app_collection_app', 'remove_sql',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'App.setup_sql'
        db.add_column('app_collection_app', 'setup_sql',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    models = {
        'app_collection.apiversion': {
            'Meta': {'object_name': 'ApiVersion'},
            'brand_version': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sdk_version': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'app_collection.app': {
            'Meta': {'object_name': 'App'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'github_account': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'github_project': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'shortname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Pending'", 'max_length': '8'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'app_collection.appinstance': {
            'Meta': {'object_name': 'AppInstance'},
            'api_version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_collection.ApiVersion']"}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_collection.App']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remove_sql': ('django.db.models.fields.TextField', [], {}),
            'setup_sql': ('django.db.models.fields.TextField', [], {}),
            'so_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app_collection']