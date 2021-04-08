from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Caida, Persona, Usuario

# Create your views here.
def validar_usuario(_cedula, clave):
    try:
        usuario = Usuario.objects.get(persona__cedula=_cedula)
        return clave == usuario.clave
    except Exception:
        return None

def login(request):
    try:
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
                        'id': persona.id,
                        'nombre': persona.nombre,
                        'apellido': persona.apellido
                    }
                    return redirect('administracion/')
                else:
                    mensaje = 'Inicio de sesión fallido. La contraseña es incorrecta.'
            else:
                mensaje = f'Inicio de sesión fallido. El usuario {_cedula} no existe'
        if request.session['esta_logueado']:
            return redirect('administracion/')
        else:
            contexto = {
                'mensaje': mensaje
            }
            return HttpResponse(html.render(contexto, request))
    except Exception:
        request.session['esta_logueado'] = False
        return redirect('/')

def logout(request):
    try:
        if request.session['esta_logueado']:
            del request.session['esta_logueado']
            del request.session['usuario_autenticado']
        return redirect('/')
    except Exception:
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
    except Exception:
        return redirect('/')

def usuarios(request):
    try:
        if request.session['esta_logueado']:
            html = loader.get_template('monitor/usuarios.html')
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
    except Exception:
        return redirect('/')

def agregar_usuario(request):
    try:
        if request.session['esta_logueado']:
            html = loader.get_template('monitor/agregar-usuario.html')
            mensaje = ''
            tipo_mensaje = ''
            if request.method == 'POST':
                _cedula = request.POST.get('cedula', '')
                resultado = Persona.objects.filter(cedula=_cedula)
                if len(resultado) == 0:
                    _persona = Persona(
                        cedula=_cedula,
                        nombre=request.POST.get('nombre', ''),
                        apellido=request.POST.get('apellido', '')
                    )
                    _persona.save()
                    usuario = Usuario(
                        persona=_persona,
                        clave=request.POST.get('clave', ''),
                        tipo=request.POST.get('tipo', '')
                    )
                    usuario.save()
                    mensaje = 'Operación exitosa. Usuario registrado correctamente.'
                    tipo_mensaje = 'exito'
                else:
                    mensaje = 'Operación fallida. El usuario ya existe.'
                    tipo_mensaje = 'error'
            contexto = {
                'usuario_autenticado': request.session['usuario_autenticado'],
                'mensaje': mensaje,
                'tipo_mensaje': tipo_mensaje
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception:
        return redirect('/')

def editar_usuario(request, _id):
    try:
        if request.session['esta_logueado']:
            html = loader.get_template('editar-usuario')
            mensaje = ''
            tipo_mensaje = ''
            persona = Usuario.objects.get(id=_id)
            usuario = Usuario.objects.get(persona__id=_id)
            if request.method == 'POST':
                persona.cedula = request.POST.get('cedula', '')
                persona.nombre = request.POST.get('nombre', '')
                persona.apellido = request.POST.get('apellido', '')
                persona.save()
                usuario.clave = request.POST.get('clave', '')
                usuario.tipo = request.POST.get('tipo', '')
                usuario.save()
            contexto = {
                'cedula': usuario.persona.cedula,
                'nombre': usuario.persona.nombre,
                'apellido': usuario.persona.apellido,
                'tipo': usuario.tipo,
                'mensaje': mensaje,
                'tipo_mensaje': tipo_mensaje
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception:
        return redirect('/')

def eliminar_usuario(request, _id):
    try:
        if request.session['esta_logueado']:
            usuario_autenticado = request.session['usuario_autenticado']
            if _id != 1 and _id != usuario_autenticado['id']:
                usuario = Persona.objects.get(id=_id)
                usuario.delete()
            return redirect('/administracion/usuarios')
        else:
            return redirect('/')
    except Exception:
        return redirect('/')
