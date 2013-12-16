#encoding:utf-8
from django.forms import ModelForm
from django import forms
from principal.models import MyUser, Pelicula, Actor, Director

class NuevoUsuarioForm(forms.Form):
	required_css_class = 'required'
	
	usuario = forms.CharField(label='Tu usuario')
	password = forms.CharField(widget=forms.PasswordInput(), label='Tu password')
	password2 = forms.CharField(widget=forms.PasswordInput(), label='Repite password')
	nombre = forms.CharField(label='Tu nombre')
	apellidos = forms.CharField(label='Tus apellidos')
	correo = forms.EmailField(label='Tu correo electronico')
	fecha_nacimiento = forms.DateField(label='Tu fecha de ancimento', required=False)
	avatar = forms.ImageField(required=False)
	
	def clean(self):
		cleaned_data = super(NuevoUsuarioForm, self).clean()
		password = cleaned_data.get("password")
		password2 = cleaned_data.get("password2")
		correo = cleaned_data.get("correo")
		usuario = cleaned_data.get("usuario")

		if password != password2:
			msg = u"Las contraseñas deben coincidir"
			self._errors["password"] = self.error_class([msg])
			self._errors["password2"] = self.error_class([msg])

			del cleaned_data["password"]
			del cleaned_data["password2"]

		if MyUser.objects.filter(email=correo).exists():
			msg = u"El email ya existe"
			self._errors["correo"] = self.error_class([msg])

			del cleaned_data["correo"]

		if MyUser.objects.filter(usuario=usuario).exists():
			msg = u"El usuario ya existe"
			self._errors["usuario"] = self.error_class([msg])

			del cleaned_data["usuario"]

		return cleaned_data

class ContactoForm(forms.Form):
	required_css_class = 'required'
	
	nombre = forms.CharField(label='Tu nombre')
	correo = forms.EmailField(label='Tu correo electronico')
	consulta = forms.CharField(widget=forms.Textarea)

class SubirPelicula(ModelForm):
	class Meta:
		model = Pelicula
		exclude = ['votaciones', 'comentarios']

class SubirActor(ModelForm):
	class Meta:
		model = Actor
		exclude = ['comentarios']

class SubirDirector(ModelForm):
	class Meta:
		model = Director
		exclude = ['comentarios']