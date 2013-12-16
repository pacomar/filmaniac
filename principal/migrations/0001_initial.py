# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Categoria'
        db.create_table(u'principal_categoria', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'principal', ['Categoria'])

        # Adding model 'Pais'
        db.create_table(u'principal_pais', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'principal', ['Pais'])

        # Adding model 'Contacto'
        db.create_table(u'principal_contacto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('correo', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('consulta', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'principal', ['Contacto'])

        # Adding model 'MyUser'
        db.create_table(u'principal_myuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('apellidos', self.gf('django.db.models.fields.CharField')(max_length=180, null=True, blank=True)),
            ('usuario', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('fecha_nacimiento', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(default='avatar.jpg', max_length=100, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'principal', ['MyUser'])

        # Adding M2M table for field groups on 'MyUser'
        m2m_table_name = db.shorten_name(u'principal_myuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('myuser', models.ForeignKey(orm[u'principal.myuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['myuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'MyUser'
        m2m_table_name = db.shorten_name(u'principal_myuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('myuser', models.ForeignKey(orm[u'principal.myuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['myuser_id', 'permission_id'])

        # Adding M2M table for field cat_preferidas on 'MyUser'
        m2m_table_name = db.shorten_name(u'principal_myuser_cat_preferidas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('myuser', models.ForeignKey(orm[u'principal.myuser'], null=False)),
            ('categoria', models.ForeignKey(orm[u'principal.categoria'], null=False))
        ))
        db.create_unique(m2m_table_name, ['myuser_id', 'categoria_id'])

        # Adding model 'Votacion'
        db.create_table(u'principal_votacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voto', self.gf('django.db.models.fields.IntegerField')()),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['principal.MyUser'])),
        ))
        db.send_create_signal(u'principal', ['Votacion'])

        # Adding model 'Mensaje'
        db.create_table(u'principal_mensaje', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fro', self.gf('django.db.models.fields.related.ForeignKey')(related_name='remitente', to=orm['principal.MyUser'])),
            ('to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='destinatario', to=orm['principal.MyUser'])),
            ('fecha_envio', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('mensaje', self.gf('django.db.models.fields.TextField')()),
            ('leido', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'principal', ['Mensaje'])

        # Adding model 'Comentario'
        db.create_table(u'principal_comentario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('autor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['principal.MyUser'])),
            ('comentario', self.gf('django.db.models.fields.TextField')()),
            ('fecha_creacion', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('fecha_modificacion', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'principal', ['Comentario'])

        # Adding model 'Director'
        db.create_table(u'principal_director', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('apellidos', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('fecha_nacimiento', self.gf('django.db.models.fields.DateField')()),
            ('nacionalidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['principal.Pais'])),
            ('biografia', self.gf('django.db.models.fields.TextField')()),
            ('foto', self.gf('django.db.models.fields.files.ImageField')(default='avatar.jpg', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'principal', ['Director'])

        # Adding M2M table for field comentarios on 'Director'
        m2m_table_name = db.shorten_name(u'principal_director_comentarios')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('director', models.ForeignKey(orm[u'principal.director'], null=False)),
            ('comentario', models.ForeignKey(orm[u'principal.comentario'], null=False))
        ))
        db.create_unique(m2m_table_name, ['director_id', 'comentario_id'])

        # Adding model 'Actor'
        db.create_table(u'principal_actor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('apellidos', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('fecha_nacimiento', self.gf('django.db.models.fields.DateField')()),
            ('nacionalidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['principal.Pais'])),
            ('biografia', self.gf('django.db.models.fields.TextField')()),
            ('foto', self.gf('django.db.models.fields.files.ImageField')(default='avatar.jpg', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'principal', ['Actor'])

        # Adding M2M table for field comentarios on 'Actor'
        m2m_table_name = db.shorten_name(u'principal_actor_comentarios')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('actor', models.ForeignKey(orm[u'principal.actor'], null=False)),
            ('comentario', models.ForeignKey(orm[u'principal.comentario'], null=False))
        ))
        db.create_unique(m2m_table_name, ['actor_id', 'comentario_id'])

        # Adding model 'Pelicula'
        db.create_table(u'principal_pelicula', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('anio', self.gf('django.db.models.fields.DateField')()),
            ('director', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['principal.Director'])),
            ('resumen', self.gf('django.db.models.fields.TextField')()),
            ('caratula', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'principal', ['Pelicula'])

        # Adding M2M table for field reparto on 'Pelicula'
        m2m_table_name = db.shorten_name(u'principal_pelicula_reparto')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pelicula', models.ForeignKey(orm[u'principal.pelicula'], null=False)),
            ('actor', models.ForeignKey(orm[u'principal.actor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pelicula_id', 'actor_id'])

        # Adding M2M table for field categorias on 'Pelicula'
        m2m_table_name = db.shorten_name(u'principal_pelicula_categorias')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pelicula', models.ForeignKey(orm[u'principal.pelicula'], null=False)),
            ('categoria', models.ForeignKey(orm[u'principal.categoria'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pelicula_id', 'categoria_id'])

        # Adding M2M table for field votaciones on 'Pelicula'
        m2m_table_name = db.shorten_name(u'principal_pelicula_votaciones')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pelicula', models.ForeignKey(orm[u'principal.pelicula'], null=False)),
            ('votacion', models.ForeignKey(orm[u'principal.votacion'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pelicula_id', 'votacion_id'])

        # Adding M2M table for field comentarios on 'Pelicula'
        m2m_table_name = db.shorten_name(u'principal_pelicula_comentarios')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pelicula', models.ForeignKey(orm[u'principal.pelicula'], null=False)),
            ('comentario', models.ForeignKey(orm[u'principal.comentario'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pelicula_id', 'comentario_id'])


    def backwards(self, orm):
        # Deleting model 'Categoria'
        db.delete_table(u'principal_categoria')

        # Deleting model 'Pais'
        db.delete_table(u'principal_pais')

        # Deleting model 'Contacto'
        db.delete_table(u'principal_contacto')

        # Deleting model 'MyUser'
        db.delete_table(u'principal_myuser')

        # Removing M2M table for field groups on 'MyUser'
        db.delete_table(db.shorten_name(u'principal_myuser_groups'))

        # Removing M2M table for field user_permissions on 'MyUser'
        db.delete_table(db.shorten_name(u'principal_myuser_user_permissions'))

        # Removing M2M table for field cat_preferidas on 'MyUser'
        db.delete_table(db.shorten_name(u'principal_myuser_cat_preferidas'))

        # Deleting model 'Votacion'
        db.delete_table(u'principal_votacion')

        # Deleting model 'Mensaje'
        db.delete_table(u'principal_mensaje')

        # Deleting model 'Comentario'
        db.delete_table(u'principal_comentario')

        # Deleting model 'Director'
        db.delete_table(u'principal_director')

        # Removing M2M table for field comentarios on 'Director'
        db.delete_table(db.shorten_name(u'principal_director_comentarios'))

        # Deleting model 'Actor'
        db.delete_table(u'principal_actor')

        # Removing M2M table for field comentarios on 'Actor'
        db.delete_table(db.shorten_name(u'principal_actor_comentarios'))

        # Deleting model 'Pelicula'
        db.delete_table(u'principal_pelicula')

        # Removing M2M table for field reparto on 'Pelicula'
        db.delete_table(db.shorten_name(u'principal_pelicula_reparto'))

        # Removing M2M table for field categorias on 'Pelicula'
        db.delete_table(db.shorten_name(u'principal_pelicula_categorias'))

        # Removing M2M table for field votaciones on 'Pelicula'
        db.delete_table(db.shorten_name(u'principal_pelicula_votaciones'))

        # Removing M2M table for field comentarios on 'Pelicula'
        db.delete_table(db.shorten_name(u'principal_pelicula_comentarios'))


    models = {
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'principal.actor': {
            'Meta': {'object_name': 'Actor'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'biografia': ('django.db.models.fields.TextField', [], {}),
            'comentarios': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['principal.Comentario']", 'null': 'True', 'blank': 'True'}),
            'fecha_nacimiento': ('django.db.models.fields.DateField', [], {}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'default': "'avatar.jpg'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nacionalidad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['principal.Pais']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'principal.categoria': {
            'Meta': {'object_name': 'Categoria'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'principal.comentario': {
            'Meta': {'object_name': 'Comentario'},
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['principal.MyUser']"}),
            'comentario': ('django.db.models.fields.TextField', [], {}),
            'fecha_creacion': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_modificacion': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'principal.contacto': {
            'Meta': {'object_name': 'Contacto'},
            'consulta': ('django.db.models.fields.TextField', [], {}),
            'correo': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'principal.director': {
            'Meta': {'object_name': 'Director'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'biografia': ('django.db.models.fields.TextField', [], {}),
            'comentarios': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['principal.Comentario']", 'null': 'True', 'blank': 'True'}),
            'fecha_nacimiento': ('django.db.models.fields.DateField', [], {}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'default': "'avatar.jpg'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nacionalidad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['principal.Pais']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'principal.mensaje': {
            'Meta': {'object_name': 'Mensaje'},
            'fecha_envio': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fro': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'remitente'", 'to': u"orm['principal.MyUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mensaje': ('django.db.models.fields.TextField', [], {}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destinatario'", 'to': u"orm['principal.MyUser']"})
        },
        u'principal.myuser': {
            'Meta': {'object_name': 'MyUser'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '180', 'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "'avatar.jpg'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cat_preferidas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['principal.Categoria']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'fecha_nacimiento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'usuario': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'principal.pais': {
            'Meta': {'object_name': 'Pais'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'principal.pelicula': {
            'Meta': {'object_name': 'Pelicula'},
            'anio': ('django.db.models.fields.DateField', [], {}),
            'caratula': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'categorias': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['principal.Categoria']", 'symmetrical': 'False'}),
            'comentarios': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['principal.Comentario']", 'null': 'True', 'blank': 'True'}),
            'director': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['principal.Director']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reparto': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['principal.Actor']", 'symmetrical': 'False'}),
            'resumen': ('django.db.models.fields.TextField', [], {}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'votaciones': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['principal.Votacion']", 'null': 'True', 'blank': 'True'})
        },
        u'principal.votacion': {
            'Meta': {'object_name': 'Votacion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['principal.MyUser']"}),
            'voto': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['principal']