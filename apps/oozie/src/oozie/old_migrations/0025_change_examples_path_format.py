# -*- coding: utf-8 -*-
import datetime
import json
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):
    needed_by = (
        ("desktop", "0007_auto__add_documentpermission__add_documenttag__add_document"),
    )

    def forwards(self, orm):
        """Migrate from ["path1", "path2", ...] to [{"name":"path1"},{"name":"path2"},...]"""
        for fs in orm.Fs.objects.all():
            new_mkdirs = []
            for mkdir in json.loads(fs.mkdirs):
                if isinstance(mkdir, basestring):
                    new_mkdirs.append({'name': mkdir})

            new_touchzs = []
            for touchzs in json.loads(fs.touchzs):
                if isinstance(touchzs, basestring):
                    new_touchzs.append({'name': touchzs})

            if new_mkdirs:
                fs.mkdirs = json.dumps(new_mkdirs)

            if new_touchzs:
                fs.touchzs = json.dumps(new_touchzs)

            fs.save()

    def backwards(self, orm):
        """Migrate from [{"name":"path1"},{"name":"path2"},...] to ["path1", "path2", ...]"""
        for fs in orm.Fs.objects.all():
            new_mkdirs = []
            for mkdir in json.loads(fs.mkdirs):
                if isinstance(mkdir, dict) and 'name' in mkdir:
                    new_mkdirs.append(mkdir['name'])

            new_touchzs = []
            for touchzs in json.loads(fs.touchzs):
                if isinstance(touchzs, dict) and 'name' in touchzs:
                    new_touchzs.append(touchzs['name'])

            if new_mkdirs:
                fs.mkdirs = json.dumps(new_mkdirs)

            if new_touchzs:
                fs.touchzs = json.dumps(new_touchzs)

            fs.save()

    models = {
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
        },
        'desktop.document': {
            'Meta': {'object_name': 'Document'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'extra': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'doc_owner'", 'to': "orm['auth.User']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['desktop.DocumentTag']", 'db_index': 'True', 'symmetrical': 'False'}),
            'version': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'desktop.documenttag': {
            'Meta': {'object_name': 'DocumentTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'tag': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'oozie.bundle': {
            'Meta': {'object_name': 'Bundle', '_ormbases': ['oozie.Job']},
            'coordinators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['oozie.Coordinator']", 'through': "orm['oozie.BundledCoordinator']", 'symmetrical': 'False'}),
            'job_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Job']", 'unique': 'True', 'primary_key': 'True'}),
            'kick_off_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 20, 0, 0)'})
        },
        'oozie.bundledcoordinator': {
            'Meta': {'object_name': 'BundledCoordinator'},
            'bundle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oozie.Bundle']"}),
            'coordinator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oozie.Coordinator']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameters': ('django.db.models.fields.TextField', [], {'default': '\'[{"name":"oozie.use.system.libpath","value":"true"}]\''})
        },
        'oozie.coordinator': {
            'Meta': {'object_name': 'Coordinator', '_ormbases': ['oozie.Job']},
            'concurrency': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 23, 0, 0)'}),
            'execution': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'frequency_number': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'frequency_unit': ('django.db.models.fields.CharField', [], {'default': "'days'", 'max_length': '20'}),
            'job_properties': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Job']", 'unique': 'True', 'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 20, 0, 0)'}),
            'throttle': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timeout': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'America/Los_Angeles'", 'max_length': '24'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oozie.Workflow']", 'null': 'True'})
        },
        'oozie.datainput': {
            'Meta': {'object_name': 'DataInput'},
            'coordinator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oozie.Coordinator']"}),
            'dataset': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Dataset']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'oozie.dataoutput': {
            'Meta': {'object_name': 'DataOutput'},
            'coordinator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oozie.Coordinator']"}),
            'dataset': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Dataset']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'oozie.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'advanced_end_instance': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '128', 'blank': 'True'}),
            'advanced_start_instance': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '128'}),
            'coordinator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oozie.Coordinator']"}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'done_flag': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'frequency_number': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'frequency_unit': ('django.db.models.fields.CharField', [], {'default': "'days'", 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_choice': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 20, 0, 0)'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'America/Los_Angeles'", 'max_length': '24'}),
            'uri': ('django.db.models.fields.CharField', [], {'default': "'/data/${YEAR}${MONTH}${DAY}'", 'max_length': '1024'})
        },
        'oozie.decision': {
            'Meta': {'object_name': 'Decision'},
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'})
        },
        'oozie.decisionend': {
            'Meta': {'object_name': 'DecisionEnd'},
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'})
        },
        'oozie.distcp': {
            'Meta': {'object_name': 'DistCp'},
            'job_properties': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_xml': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'params': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'prepares': ('django.db.models.fields.TextField', [], {'default': "'[]'"})
        },
        'oozie.email': {
            'Meta': {'object_name': 'Email'},
            'body': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'cc': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'subject': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'to': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        'oozie.end': {
            'Meta': {'object_name': 'End'},
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'})
        },
        'oozie.fork': {
            'Meta': {'object_name': 'Fork'},
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'})
        },
        'oozie.fs': {
            'Meta': {'object_name': 'Fs'},
            'chmods': ('django.db.models.fields.TextField', [], {'default': "'[]'", 'blank': 'True'}),
            'deletes': ('django.db.models.fields.TextField', [], {'default': "'[]'", 'blank': 'True'}),
            'mkdirs': ('django.db.models.fields.TextField', [], {'default': "'[]'", 'blank': 'True'}),
            'moves': ('django.db.models.fields.TextField', [], {'default': "'[]'", 'blank': 'True'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'touchzs': ('django.db.models.fields.TextField', [], {'default': "'[]'", 'blank': 'True'})
        },
        'oozie.generic': {
            'Meta': {'object_name': 'Generic'},
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'xml': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        'oozie.history': {
            'Meta': {'object_name': 'History'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oozie.Job']"}),
            'oozie_job_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'properties': ('django.db.models.fields.TextField', [], {}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oozie.hive': {
            'Meta': {'object_name': 'Hive'},
            'archives': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'files': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_properties': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_xml': ('django.db.models.fields.CharField', [], {'default': "'hive-config.xml'", 'max_length': '512', 'blank': 'True'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'params': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'prepares': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'script_path': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'oozie.java': {
            'Meta': {'object_name': 'Java'},
            'archives': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'args': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'capture_output': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'files': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'jar_path': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'java_opts': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'job_properties': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_xml': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'main_class': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'prepares': ('django.db.models.fields.TextField', [], {'default': "'[]'"})
        },
        'oozie.job': {
            'Meta': {'object_name': 'Job'},
            'data': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
            'deployment_dir': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shared': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'parameters': ('django.db.models.fields.TextField', [], {'default': '\'[{"name":"oozie.use.system.libpath","value":"true"}]\''}),
            'schema_version': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'oozie.join': {
            'Meta': {'object_name': 'Join'},
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'})
        },
        'oozie.kill': {
            'Meta': {'object_name': 'Kill'},
            'message': ('django.db.models.fields.CharField', [], {'default': "'Action failed, error message[${wf:errorMessage(wf:lastErrorNode())}]'", 'max_length': '256'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'})
        },
        'oozie.link': {
            'Meta': {'object_name': 'Link'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_node'", 'to': "orm['oozie.Node']"}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_node'", 'to': "orm['oozie.Node']"})
        },
        'oozie.mapreduce': {
            'Meta': {'object_name': 'Mapreduce'},
            'archives': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'files': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'jar_path': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'job_properties': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_xml': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'prepares': ('django.db.models.fields.TextField', [], {'default': "'[]'"})
        },
        'oozie.node': {
            'Meta': {'object_name': 'Node'},
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'parents'", 'symmetrical': 'False', 'through': "orm['oozie.Link']", 'to': "orm['oozie.Node']"}),
            'data': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'node_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oozie.Workflow']"})
        },
        'oozie.pig': {
            'Meta': {'object_name': 'Pig'},
            'archives': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'files': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_properties': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_xml': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'params': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'prepares': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'script_path': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'oozie.shell': {
            'Meta': {'object_name': 'Shell'},
            'archives': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'capture_output': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'command': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'files': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_properties': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_xml': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'params': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'prepares': ('django.db.models.fields.TextField', [], {'default': "'[]'"})
        },
        'oozie.sqoop': {
            'Meta': {'object_name': 'Sqoop'},
            'archives': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'files': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_properties': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_xml': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'params': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'prepares': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'script_path': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'oozie.ssh': {
            'Meta': {'object_name': 'Ssh'},
            'capture_output': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'command': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'params': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'oozie.start': {
            'Meta': {'object_name': 'Start'},
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'})
        },
        'oozie.streaming': {
            'Meta': {'object_name': 'Streaming'},
            'archives': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'files': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_properties': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'mapper': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'reducer': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'oozie.subworkflow': {
            'Meta': {'object_name': 'SubWorkflow'},
            'job_properties': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'propagate_configuration': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sub_workflow': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['oozie.Workflow']", 'null': 'True', 'blank': 'True'})
        },
        'oozie.workflow': {
            'Meta': {'object_name': 'Workflow', '_ormbases': ['oozie.Job']},
            'end': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'end_workflow'", 'null': 'True', 'to': "orm['oozie.End']"}),
            'is_single': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_properties': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'job_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['oozie.Job']", 'unique': 'True', 'primary_key': 'True'}),
            'job_xml': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'managed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'start_workflow'", 'null': 'True', 'to': "orm['oozie.Start']"})
        }
    }

    complete_apps = ['oozie']
    symmetrical = True
