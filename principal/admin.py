from django.contrib import admin
from principal.models import Categoria, Pelicula, MyUser, Votacion, Actor, Director, Contacto, Pais, Mensaje, Comentario

admin.site.register(MyUser)
admin.site.register(Pelicula)
admin.site.register(Categoria)
admin.site.register(Votacion)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Contacto)
admin.site.register(Pais)
admin.site.register(Mensaje)
admin.site.register(Comentario)