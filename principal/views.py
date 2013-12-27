from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from principal.forms import NuevoUsuarioForm, ContactoForm, SubirActor, SubirPelicula, SubirDirector, Comenta, EnviaMensaje, Responde, BuscaWikipedia
from principal.models import MyUser, Pelicula, Actor, Categoria, Director, Votacion, Contacto, Comentario, Mensaje
from django.contrib.auth.decorators import login_required
import datetime

def calcula_edad(fecha):
    hoy = datetime.date.today()
    return ((hoy - fecha)/365).days

def index(request):
    if request.user.is_authenticated():
            ctx = {}
            return render(request, 'privada.html', ctx)
    else:
            ctx = {}
            return render(request, 'publica.html', ctx)

def registro(request):
    if request.method=='POST':
            formulario=NuevoUsuarioForm(request.POST)
            if formulario.is_valid():
                    usern = formulario.cleaned_data['usuario']
                    passw = formulario.cleaned_data['password']
                    passw2 = formulario.cleaned_data['password2']
                    nom = formulario.cleaned_data['nombre']
                    ape = formulario.cleaned_data['apellidos']
                    ema = formulario.cleaned_data['correo']
                    fecha_nacimiento = formulario.cleaned_data['fecha_nacimiento']
                    ava = formulario.cleaned_data['avatar']
                    MyUser.objects.create_user(usuario=usern, password=passw, nombre=nom, apellidos=ape, email=ema, fecha_nacimiento=fecha_nacimiento, avatar=ava)
                    return HttpResponseRedirect('/')
    else:
            formulario = NuevoUsuarioForm()
    ctx = {'formulario':formulario}
    return render(request, 'registro.html',ctx)

def entrar(request):
    if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                    usuario = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    user = authenticate(usuario=usuario, password=password)
                    if user is not None and user.is_active:
                            login(request, user)
                            return redirect('/privada')
                    else:
                            return HttpResponse('Algo salio mal')
            else:
                    return HttpResponse('El formulario no es valido')
    else:
            form = AuthenticationForm()
    ctx = {'form':form}
    return render(request, 'login.html', ctx)

def contacto(request):
    if request.method=='POST':
            formulario=ContactoForm(request.POST)
            if formulario.is_valid():
                    nom = formulario.cleaned_data['nombre']
                    ema = formulario.cleaned_data['correo']
                    consulta = formulario.cleaned_data['consulta']
                    Contacto.objects.create(nombre=nom, correo=ema, consulta=consulta)
                    return HttpResponseRedirect('/')
    else:
            formulario = ContactoForm()
    ctx = {'formulario':formulario}
    return render(request, 'contacto.html',ctx)

@login_required(login_url='/login')
def privada(request):
    ctx = {}
    return render(request, 'privada.html', ctx)

@login_required(login_url='/login')
def exit(request):
    logout(request)
    ctx = {}
    return render(request, 'publica.html', ctx)

@login_required(login_url='/login')
def peliculas(request):
    peliculas = Pelicula.objects.all()
    ctx = {'pelis':peliculas}
    return render(request, 'peliculas.html', ctx)

@login_required(login_url='/login')
def pelicula(request, id_pelicula):
    peli = Pelicula.objects.get(id=id_pelicula)
    acum = 0.0
    for v in peli.votaciones.all():
             acum = acum + v.voto
    puntuacion = 0
    voto = None
    if peli.votaciones.count() > 0:
            puntuacion = acum / peli.votaciones.count()
            if peli.votaciones.filter(usuario=request.user):
                voto = peli.votaciones.get(usuario=request.user)
    ctx = {'pelicula':peli,'puntuacion':puntuacion,'voto':voto}
    return render(request, 'pelicula.html', ctx)

@login_required(login_url='/login')
def actores(request):
    actores = Actor.objects.all()
    ctx = {'actores':actores}
    return render(request, 'actores.html', ctx)

@login_required(login_url='/login')
def actor(request, id_actor):
    actor = Actor.objects.get(id=id_actor)
    peliculas = Pelicula.objects.filter(reparto=id_actor)
    ctx = {'actor':actor, 'peliculas':peliculas, 'edad':calcula_edad(actor.fecha_nacimiento)}
    return render(request, 'actor.html', ctx)

@login_required(login_url='/login')
def perfil(request, user_usuario):
    usuario = MyUser.objects.get(usuario=user_usuario)
    ctx = {'user':usuario, 'edad':calcula_edad(usuario.fecha_nacimiento)}
    return render(request, 'perfil.html', ctx)

@login_required(login_url='/login')
def mi_perfil(request):
    usuario = MyUser.objects.get(usuario=request.user.usuario)
    mensajes = Mensaje.objects.filter(to=request.user)
    ctx = {'user':usuario, 'edad':calcula_edad(usuario.fecha_nacimiento), 'mensajes':mensajes.reverse()}
    return render(request, 'perfil.html', ctx)

@login_required(login_url='/login')
def categorias(request):
    categorias = Categoria.objects.all()
    ctx = {'categorias':categorias}
    return render(request, 'categorias.html', ctx)

@login_required(login_url='/login')
def categoria(request, id_categoria):
    categoria = Categoria.objects.get(id=id_categoria)
    peliculas = Pelicula.objects.filter(categorias=id_categoria)
    ctx = {'peliculas':peliculas,'categoria':categoria}
    return render(request, 'categoria.html', ctx)

@login_required(login_url='/login')
def directores(request):
    directores = Director.objects.all()
    ctx = {'directores':directores}
    return render(request, 'directores.html', ctx)

@login_required(login_url='/login')
def director(request, id_director):
    director = Director.objects.get(id=id_director)
    peliculas = Pelicula.objects.filter(director=id_director)
    ctx = {'director':director, 'peliculas':peliculas, 'edad':calcula_edad(director.fecha_nacimiento)}
    return render(request, 'director.html', ctx)

@login_required(login_url='/login')
def vota(request, id_pelicula):
    num = request.POST.get("valoracion")
    user = request.user
    voto = Votacion(voto=num,usuario=user)
    voto.save()
    Pelicula.objects.get(id=id_pelicula).votaciones.add(voto)
    return HttpResponseRedirect('/pelicula/'+id_pelicula)

@login_required(login_url='/login')
def eliminavoto(request, id_voto):
    peli = Pelicula.objects.get(votaciones=id_voto)
    voto = Votacion.objects.get(id=id_voto)
    if request.user == voto.usuario:
            voto.delete()
    return HttpResponseRedirect('/pelicula/'+str(peli.id))

@login_required(login_url='/login')
def contribuir(request):
    ctx = {}
    return render(request, 'contribuir.html', ctx)

@login_required(login_url='/login')
def nueva_pelicula(request):
    if request.method == 'POST':
        formulario = SubirPelicula(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('/peliculas')
    else:
        formulario = SubirPelicula()
    ctx = {'formulario':formulario}
    return render(request, 'nueva_pelicula.html', ctx)

@login_required(login_url='/login')
def nuevo_actor(request):
    if request.method == 'POST':
        formulario = SubirActor(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('/actores')
    else:
        formulario = SubirActor()
    ctx = {'formulario':formulario}
    return render(request, 'nuevo_actor.html', ctx)

@login_required(login_url='/login')
def nuevo_director(request):
    if request.method == 'POST':
        formulario = SubirDirector(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('/directores')
    else:
        formulario = SubirDirector()
    ctx = {'formulario':formulario}
    return render(request, 'nuevo_director.html', ctx)

@login_required(login_url='/login')
def comenta_actor(request, id_actor):
    if request.method == 'POST':
        formulario = Comenta(request.POST)
        if formulario.is_valid():
            autor = request.user
            com = formulario.cleaned_data['comentario']
            comen = Comentario.objects.create(autor=autor, comentario=com)
            actor = Actor.objects.get(id=id_actor)
            actor.comentarios.add(comen)
            return redirect('/actor/'+str(actor.id))
    else:
        formulario = Comenta()
    ctx = {'formulario':formulario}
    return render(request, 'privada.html', ctx)

@login_required(login_url='/login')
def comenta_director(request, id_director):
    if request.method == 'POST':
        formulario = Comenta(request.POST)
        if formulario.is_valid():
            autor = request.user
            com = formulario.cleaned_data['comentario']
            comen = Comentario.objects.create(autor=autor, comentario=com)
            director = Director.objects.get(id=id_director)
            director.comentarios.add(comen)
            return redirect('/director/'+str(director.id))
    else:
        formulario = Comenta()
    ctx = {'formulario':formulario}
    return render(request, 'privada.html', ctx)

@login_required(login_url='/login')
def comenta_pelicula(request, id_pelicula):
    if request.method == 'POST':
        formulario = Comenta(request.POST)
        if formulario.is_valid():
            autor = request.user
            com = formulario.cleaned_data['comentario']
            comen = Comentario.objects.create(autor=autor, comentario=com)
            pelicula = Pelicula.objects.get(id=id_pelicula)
            pelicula.comentarios.add(comen)
            return redirect('/pelicula/'+str(pelicula.id))
    return redirect('/error/')

@login_required(login_url='/login')
def envia_mensaje(request, user_usuario):
    if request.method == 'POST':
        formulario = Responde(request.POST)
        if formulario.is_valid():
            fro = request.user
            to = MyUser.objects.get(usuario=user_usuario)
            asu = formulario.cleaned_data['asunto']
            men = formulario.cleaned_data['mensaje']
            mensaje = Mensaje.objects.create(to=to, fro=fro, asunto=asu, mensaje=men)
            return redirect('/miperfil/')
    return redirect('/error/')

@login_required(login_url='/login')
def error(request):
    ctx = {}
    return render(request, 'error.html', ctx)


from pattern.web import Wikipedia
engine = Wikipedia(license=None, throttle=5.0, language='es')
@login_required(login_url='/login')
def busca_wikipedia(request):
    if request.method == 'POST':
        formulario = BuscaWikipedia(request.POST)
        if formulario.is_valid():
            busca = formulario.cleaned_data['busca']
            article = engine.search(busca)
            ctx = {'articulo':article}
            return render(request, 'wikipedia.html', ctx)
    return redirect('/error/')

@login_required(login_url='/login')
def busca_wikipedia2(request, campo):
    article = engine.search(campo)
    ctx = {'articulo':article}
    return render(request, 'wikipedia.html', ctx)