from django.conf.urls import patterns, include, url, i18n
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'principal.views.index', name='home'),
    url(r'^registro/', 'principal.views.registro'),
    url(r'^login/', 'principal.views.entrar'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^privada/', 'principal.views.privada'),
    url(r'^salir/', 'principal.views.exit'),
    url(r'^peliculas/', 'principal.views.peliculas'),
    url(r'^pelicula/(?P<id_pelicula>\d+)$','principal.views.pelicula'),
    url(r'^actores/', 'principal.views.actores'),
    url(r'^actor/(?P<id_actor>\d+)$','principal.views.actor'),
    url(r'^categorias/', 'principal.views.categorias'),
    url(r'^categoria/(?P<id_categoria>\d+)$','principal.views.categoria'),
    url(r'^directores/', 'principal.views.directores'),
    url(r'^director/(?P<id_director>\d+)$','principal.views.director'),
    url(r'^perfil/(?P<user_usuario>\w+)$','principal.views.perfil'),
    url(r'^miperfil/','principal.views.mi_perfil'),
    url(r'^vota/(?P<id_pelicula>\d+)$', 'principal.views.vota'),
    url(r'^eliminavoto/(?P<id_voto>\d+)$', 'principal.views.eliminavoto'),
    url(r'^contribuir/', 'principal.views.contribuir'),
    url(r'^nuevapelicula/', 'principal.views.nueva_pelicula'),
    url(r'^nuevoactor/', 'principal.views.nuevo_actor'),
    url(r'^nuevodirector/', 'principal.views.nuevo_director'),
    url(r'^contacto/', 'principal.views.contacto'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
    url(r'^comenta_actor/(?P<id_actor>\d+)$','principal.views.comenta_actor'),
    url(r'^comenta_director/(?P<id_director>\d+)$','principal.views.comenta_director'),
    url(r'^comenta_pelicula/(?P<id_pelicula>\d+)$','principal.views.comenta_pelicula'),
    url(r'^enviamensaje/(?P<user_usuario>\w+)$','principal.views.envia_mensaje')
)