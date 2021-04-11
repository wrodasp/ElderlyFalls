from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Persona, Usuario, Contacto, Paciente, Caida

def validar_usuario(correo, clave):
    try:
        usuario = Usuario.objects.get(correo=correo)
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
                correo = request.POST.get('correo', '')
                clave = request.POST.get('clave', '')
                usuario_valido = validar_usuario(correo, clave)
                if usuario_valido is not None:
                    if usuario_valido:
                        usuario = Usuario.objects.select_related().get(correo=correo)
                        request.session['usuario_autenticado'] = usuario.__json__()
                        return redirect('administracion/')
                    else:
                        mensaje = 'Inicio de sesión fallido. La contraseña es incorrecta.'
                else:
                    mensaje = f'Inicio de sesión fallido. El usuario {correo} no existe'
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
            resultado = Caida.objects.select_related().all()
            caidas = [caida.__json__() for caida in resultado]
            contexto = {
                'caidas': caidas,
                'total_caidas': len(caidas),
                'tabla_vacia': range(10),
                'usuario_autenticado': request.session['usuario_autenticado']
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception as e:
        print(e)
        #return redirect('/')

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
                _correo = request.POST.get('correo', '')
                usuarios = Usuario.objects.filter(correo=_correo)
                if len(usuarios) == 0:
                    _cedula = request.POST.get('cedula', '')
                    personas = Persona.objects.filter(cedula=_cedula)
                    pacientes = Paciente.objects.select_related().filter(persona__cedula=_cedula)
                    if len(personas) == 0 and len(pacientes) == 0:
                        _persona = Persona(
                            cedula=_cedula,
                            nombre=request.POST.get('nombre', ''),
                            apellido=request.POST.get('apellido', '')
                        )
                    else:
                        mensaje = 'Operación fallida. Esta persona es un paciente.'
                        tipo_mensaje = 'error'
                        _persona.save()
                    usuario = Usuario(
                        persona=_persona,
                        correo=_correo,
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
            usuario = Usuario.objects.select_related().get(id=_id)
            if request.method == 'POST':
                try:
                    persona = usuario.persona
                    persona.nombre = request.POST.get('nombre', '')
                    persona.apellido = request.POST.get('apellido', '')
                    persona.save()
                    usuario.correo = request.POST.get('correo', '')
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
        return redirect('/')

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
            pacientes = Paciente.objects.all()
            contexto = {
                'usuario_autenticado': request.session['usuario_autenticado'],
                'pacientes': pacientes
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception as e:
        return redirect('/')

def agregar_paciente(request):
    try:
        if request.session['usuario_autenticado'] is not None:
            html = loader.get_template('monitor/agregar-paciente.html')
            mensaje = ''
            tipo_mensaje = ''

            if request.method == 'POST':
                pass
            contexto = {
                'usuario_autenticado': request.session['usuario_autenticado'],

                'mensaje': mensaje,
                'tipo_mensaje': tipo_mensaje
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception as e:
        print(e)

def editar_paciente(request, _id):
    try:
        if request.session['usuario_autenticado'] is not None:
            html = loader.get_template('monitor/editar-paciente.html')
            mensaje = ''
            tipo_mensaje = ''

            if request.method == 'POST':
                pass
            contexto = {
                'usuario_autenticado': request.session['usuario_autenticado'],
                'mensaje': mensaje,
                'tipo_mensaje': tipo_mensaje
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception as e:
        print(e)

def eliminar_paciente(request, _id):
    try:
        if request.session['usuario_autenticado'] is not None:
            mensaje = ''
            tipo_mensaje = ''

            if request.method == 'POST':
                pass
            contexto = {
                'usuario_autenticado': request.session['usuario_autenticado']
            }
            return redirect('/administracion/pacientes')
        else:
            return redirect('/')
    except Exception as e:
        print(e)
