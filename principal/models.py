#encoding:utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

#Categoria
class Categoria(models.Model):
	nombre = models.CharField(max_length=20, unique=True)

	def __unicode__(self):
		return self.nombre

#Pais
class Pais(models.Model):
	nombre = models.CharField(max_length=20, unique=True)

	def __unicode__(self):
		return self.nombre

#Contacto
class Contacto(models.Model):
	nombre = models.CharField(max_length=20)
	correo = models.EmailField()
	consulta = models.TextField()

	def __unicode__(self):
		return self.nombre

#Usuario
class MyUserManager(BaseUserManager):
	def _create_user(self, nombre, apellidos, usuario, email, password, fecha_nacimiento, avatar, **extra_fields):
		if not email:
			raise ValueError('El email no puede estar vacio.')
		if not nombre:
			raise ValueError("El nombre no puede estar vacio.")
		if not usuario:
			raise ValueError("El usuario no puede estar vacio.")
		if not apellidos:
			raise ValueError("Los apellidos deben completarse.")
		user = self.model(
			nombre=nombre,
			apellidos = apellidos,
			usuario=usuario,
			email=self.normalize_email(email),
			fecha_nacimiento=fecha_nacimiento,
			avatar=avatar,
		)

		user.set_password(password)
		return user

	def create_user(self, nombre, apellidos, usuario, email, password, fecha_nacimiento=None, avatar=None, **extra_fields):
		user = self._create_user(nombre, apellidos, usuario, email, password, fecha_nacimiento, avatar, **extra_fields)
		user.save(using=self._db)
		return user

	def create_superuser(self, nombre, apellidos, usuario, email, password, fecha_nacimiento=None, avatar=None, **extra_fields ):
		user = self._create_user(nombre, apellidos, usuario, email, password, fecha_nacimiento, avatar, **extra_fields)
		user.is_admin = True
		user.save(using=self._db)
		return user

class MyUser(AbstractBaseUser, PermissionsMixin):
	nombre = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=180, null=True,blank=True)
	usuario = models.CharField(max_length=20, unique=True)
	email = models.EmailField(unique=True)
	fecha_nacimiento = models.DateField(null=True,blank=True)
	cat_preferidas = models.ManyToManyField(Categoria, null=True, blank=True)
	avatar = models.ImageField(upload_to='usuarios/avatares', null=True, blank=True, default="avatar.jpg")

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'usuario'
	REQUIRED_FIELDS = ['nombre','apellidos','email']

	def get_full_name(self):
		# The user is identified by their email address
		return self.nombre+" "+self.apellidos

	def get_short_name(self):
		# The user is identified by their email address
		return self.usuario

	def __unicode__(self):
		return unicode(self.usuario)

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

#Votacion
class Votacion(models.Model):
	voto = models.IntegerField(choices = ((1,1),(2,2),(3,3),(4,4),(5,5)))
	usuario = models.ForeignKey(MyUser)
	def __unicode__(self):
		return str(self.voto)

#Contacto
class Mensaje(models.Model):
	fro = models.ForeignKey(MyUser, related_name="remitente")
	to = models.ForeignKey(MyUser, related_name="destinatario")
	fecha_envio = models.DateField(auto_now_add=True)
	asunto = models.CharField(max_length=100)
	mensaje = models.TextField()
	leido = models.BooleanField(default=False)

	def __unicode__(self):
		return self.mensaje

class Comentario(models.Model):
	autor = models.ForeignKey(MyUser)
	comentario = models.TextField()
	fecha_creacion = models.DateField(auto_now_add=True)
	fecha_modificacion = models.DateField(auto_now=True)
	def __unicode__(self):
		return self.comentario

#Director
class Director(models.Model):
	nombre = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=180)
	fecha_nacimiento = models.DateField()
	nacionalidad = models.ForeignKey('Pais')
	biografia = models.TextField()
	foto = models.ImageField(upload_to='retratos/actores', blank=True, null=True, default="avatar.jpg")
	comentarios = models.ManyToManyField('Comentario', blank=True, null=True)

	def __unicode__(self):
		return self.nombre+" "+self.apellidos

#Actor
class Actor(models.Model):
	nombre = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=180)
	fecha_nacimiento = models.DateField()
	nacionalidad = models.ForeignKey('Pais')
	biografia = models.TextField()
	foto = models.ImageField(upload_to='retratos/directores', blank=True, null=True, default="avatar.jpg")
	comentarios = models.ManyToManyField('Comentario', blank=True, null=True)

	def __unicode__(self):
		return self.nombre+" "+self.apellidos

#Pelicula
class Pelicula(models.Model):
	titulo = models.CharField(max_length=50)
	anio = models.DateField()
	reparto = models.ManyToManyField(Actor)
	director = models.ForeignKey(Director)
	resumen = models.TextField()
	categorias = models.ManyToManyField(Categoria)
	votaciones = models.ManyToManyField(Votacion, blank=True, null=True)
	caratula = models.ImageField(upload_to='caratulas', blank=True, null=True)
	comentarios = models.ManyToManyField('Comentario', blank=True, null=True)

	def __unicode__(self):
		return self.titulo
