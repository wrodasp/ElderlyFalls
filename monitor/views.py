from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Caida, Persona, Usuario

# Create your views here.
def login(request):
    html = loader.get_template('monitor/login.html')
    mensaje = ''
    if request.method == 'POST':
        _cedula = request.POST.get('cedula', '')
        clave = request.POST.get('clave', '')
        usuario_valido = validar_usuario(_cedula, clave)
        if usuario_valido is not None:
            if usuario_valido:
                persona = Persona.objects.filter(cedula=_cedula)[0]
                request.session['esta_logueado'] = True
                request.session['usuario_autenticado'] = {
                    'cedula': persona.cedula,
                    'nombre': persona.nombre,
                    'apellido': persona.apellido
                }
                return redirect('administracion/')
            else:
                mensaje = 'La contraseña es incorrecta'
        else:
            mensaje = f'El usuario {_cedula} no existe'
    else:
        try:
            if request.session['esta_logueado']:
                return redirect('administracion/')
        except Exception:
            request.session['esta_logueado'] = False
    contexto = {
        'mensaje': mensaje
    }
    return HttpResponse(html.render(contexto, request))

def logout(request):
    del request.session['esta_logueado']
    del request.session['usuario_autenticado']
    return redirect('/')

def administracion(request):
    try:
        if request.session['esta_logueado']:
            html = loader.get_template('monitor/administrador.html')
            caidas = Caida.objects.all().order_by('id')
            contexto = {
                'caidas': caidas,
                'tabla_vacia': range(10),
                'usuario_autenticado': request.session['usuario_autenticado']
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception as e:
        return redirect('/')

def usuarios(request):
    html = loader.get_template('monitor/usuarios.html')
    if request.method == 'POST':
        pass
    else:
        if request.session['esta_logueado']:
            resultado = Usuario.objects.all()
            usuarios = []
            for usuario in resultado:
                usuarios.append({
                    'id': usuario.id,
                    'cedula': usuario.persona.cedula,
                    'nombre': usuario.persona.nombre,
                    'apellido': usuario.persona.apellido,
                    'tipo': usuario.tipo,
                })
            contexto = {
                'usuario_autenticado': request.session['usuario_autenticado'],
                'usuarios': usuarios
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')

def validar_usuario(_cedula, clave):
    personas = Persona.objects.filter(cedula=_cedula)
    if len(personas) > 0:
        usuario = Usuario.objects.filter(persona=personas[0])[0]
        return clave == usuario.clave
    else:
        return None

def eliminar_usuario(request, id):
    usuario_autenticado = request.session['usuario_autenticado']
    if id != 1 and id != usuario_autenticado.id:
        usuario = Usuario.object.get(id=id)
        usuario.delete()
    return redirect('administracion/usuarios')
