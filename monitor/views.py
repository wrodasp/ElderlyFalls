from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Caida, Persona, Usuario

def validar_usuario(cedula, clave):
    try:
        usuario = Usuario.objects.get(persona__cedula=cedula)
        return clave == usuario.clave
    except Exception:
        return None

def login(request):
    try:
        if request.session['usuario_autenticado'] is not None:
            return redirect('administracion/')
        else:
            html = loader.get_template('monitor/login.html')
            mensaje = ''
            if request.method == 'POST':
                cedula = request.POST.get('cedula', '')
                clave = request.POST.get('clave', '')
                usuario_valido = validar_usuario(cedula, clave)
                if usuario_valido is not None:
                    if usuario_valido:
                        usuario = Usuario.objects.select_related().get(persona__cedula=cedula)
                        request.session['usuario_autenticado'] = usuario.__json__()
                        return redirect('administracion/')
                    else:
                        mensaje = 'Inicio de sesión fallido. La contraseña es incorrecta.'
                else:
                    mensaje = f'Inicio de sesión fallido. El usuario {cedula} no existe'
            contexto = {
                'mensaje': mensaje
            }
            return HttpResponse(html.render(contexto, request))
    except Exception:
        request.session['usuario_autenticado'] = None
        return redirect('/')

def logout(request):
    try:
        if request.session['usuario_autenticado'] is not None:
            del request.session['usuario_autenticado']
        return redirect('/')
    except Exception:
        return redirect('/')

def administracion(request):
    try:
        if request.session['usuario_autenticado'] is not None:
            html = loader.get_template('monitor/administrador.html')
            resultado = Caida.objects.all()
            caidas = [caida.__json__() for caida in resultado]
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
        if request.session['usuario_autenticado'] is not None:
            html = loader.get_template('monitor/usuarios.html')
            resultado = Usuario.objects.select_related().all()
            usuarios = [usuario.__json__() for usuario in resultado]
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
        if request.session['usuario_autenticado'] is not None:
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
        if request.session['usuario_autenticado'] is not None:
            html = loader.get_template('monitor/editar-usuario.html')
            mensaje = ''
            tipo_mensaje = ''
            persona = Persona.objects.get(id=_id)
            usuario = Usuario.objects.select_related().get(persona__id=persona.id)
            if request.method == 'POST':
                try:
                    persona.cedula = request.POST.get('cedula', '')
                    persona.nombre = request.POST.get('nombre', '')
                    persona.apellido = request.POST.get('apellido', '')
                    persona.save()
                    usuario.clave = request.POST.get('clave', '')
                    usuario.tipo = request.POST.get('tipo', '')
                    usuario.save()
                    mensaje = 'Operación exitosa. Usuario editado correctamente.'
                    tipo_mensaje = 'exito'
                except Exception:
                    mensaje = 'Operación fallida. Usuario no editado.'
                    tipo_mensaje = 'error'
            contexto = {
                'usuario_autenticado': request.session['usuario_autenticado'],
                'usuario': usuario,
                'mensaje': mensaje,
                'tipo_mensaje': tipo_mensaje
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception as e:
        print(e)
        return HttpResponse(str(e) + f'{_id}')

def eliminar_usuario(request, _id):
    try:
        if request.session['usuario_autenticado'] is not None:
            usuario_autenticado = request.session['usuario_autenticado']
            if _id != 1 and _id != usuario_autenticado['id']:
                usuario = Persona.objects.get(id=_id)
                usuario.delete()
            return redirect('/administracion/usuarios')
        else:
            return redirect('/')
    except Exception:
        return redirect('/')

def pacientes(request):
    try:
        if request.session['usuario_autenticado'] is not None:
            html = loader.get_template('monitor/pacientes.html')
            resultado = Usuario.objects.select_related().all()
            usuarios = [usuario.persona.cedula for usuario in resultado]
            pacientes = Persona.objects.exclude(cedula__in=usuarios)
            contexto = {
                'usuario_autenticado': request.session['usuario_autenticado'],
                'pacientes': pacientes
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception as e:
        print(e)

def agregar_paciente(request):
    try:
        if request.session['usuario_autenticado'] is not None:
            html = loader.get_template('monitor/agregar-paciente.html')
            mensaje = ''
            tipo_mensaje = ''
            resultado = Usuario.objects.select_related().all()
            usuarios = [usuario.__json__() for usuario in resultado]
            if request.method == 'POST':
                pass
            contexto = {
                'usuario_autenticado': request.session['usuario_autenticado'],
                'usuarios': usuarios,
                'mensaje': mensaje,
                'tipo_mensaje': tipo_mensaje
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception as e:
        print(e)
