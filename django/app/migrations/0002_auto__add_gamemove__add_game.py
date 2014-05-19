# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GameMove'
        db.create_table(u'app_gamemove', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_move', to=orm['app.Game'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_move_player', to=orm['auth.User'])),
            ('move_number', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
        ))
        db.send_create_signal(u'app', ['GameMove'])

        # Adding model 'Game'
        db.create_table(u'app_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player_start', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_player_start', to=orm['auth.User'])),
            ('player_x', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_player_x', to=orm['auth.User'])),
            ('player_o', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_player_o', to=orm['auth.User'])),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_player_winner', null=True, to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'app', ['Game'])


    def backwards(self, orm):
        # Deleting model 'GameMove'
        db.delete_table(u'app_gamemove')

        # Deleting model 'Game'
        db.delete_table(u'app_game')


    models = {
        u'app.comments': {
            'Meta': {'object_name': 'Comments'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'app.game': {
            'Meta': {'object_name': 'Game'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player_o': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_player_o'", 'to': u"orm['auth.User']"}),
            'player_start': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_player_start'", 'to': u"orm['auth.User']"}),
            'player_x': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_player_x'", 'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_player_winner'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'app.gamemove': {
            'Meta': {'object_name': 'GameMove'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_move'", 'to': u"orm['app.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'move_number': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_move_player'", 'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']