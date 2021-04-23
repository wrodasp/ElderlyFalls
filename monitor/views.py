from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Persona, Usuario, Contacto, Paciente, Caida

def es_cedula_valida(cedula):
    coeficientes  = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0
    for indice in range(len(cedula) - 1):
        resultado = int(cedula[indice]) * coeficientes[indice]
        if resultado > 9:
            suma += (resultado - 9)
        else:
            suma += resultado
    resultado = ((int(suma / 10) + 1) * 10) - suma
    if resultado  == 10:
        return int(cedula[9]) == 0
    else:
        return resultado == int(cedula[9])

def validar_credenciales(_correo, clave):
    try:
        usuario = Usuario.objects.get(correo=_correo)
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
                usuario_valido = validar_credenciales(correo, clave)
                if usuario_valido is not None:
                    if usuario_valido:
                        usuario = Usuario.objects.select_related().get(correo=correo)
                        if usuario.tipo == 'enfermero':
                            request.session['usuario_autenticado'] = usuario.__json__()
                            return redirect('administracion/')
                        else:
                            mensaje = (
                                'Inicio de sesión fallido. No se permiten\n.' +
                                'usuario que no sean enfermeros o enfermeras.'
                            )
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
        return redirect('/administracion')

def agregar_usuario(request):
    try:
        if request.session['usuario_autenticado'] is not None:
            html = loader.get_template('monitor/agregar-usuario.html')
            mensaje = ''
            tipo_mensaje = ''
            if request.method == 'POST':
                _cedula = request.POST.get('cedula', '')
                if es_cedula_valida(_cedula):
                    pacientes = Paciente.objects.filter(persona__cedula=_cedula)
                    if len(pacientes) == 0:
                        usuarios = Usuario.objects.filter(persona__cedula=_cedula)
                        if len(usuarios) == 0:
                            _correo = request.POST.get('correo', '')
                            usuarios = Usuario.objects.filter(correo=_correo)
                            if len(usuarios) == 0:
                                _telefono = request.POST.get('telefono', '')
                                usuarios = Usuario.objects.filter(telefono=_telefono)
                                if len(usuarios) == 0:
                                    _persona = Persona(
                                        cedula=_cedula,
                                        nombre=request.POST.get('nombre', ''),
                                        apellido=request.POST.get('apellido', '')
                                    )
                                    _persona.save()
                                    _usuario = Usuario(
                                        persona=_persona,
                                        correo=_correo,
                                        telefono=_telefono,
                                        clave=request.POST.get('clave', ''),
                                        tipo=request.POST.get('tipo', '')
                                    )
                                    _usuario.save()
                                    mensaje = 'Operación exitosa. Usuario registrado correctamente.'
                                    tipo_mensaje = 'exito'
                                else:
                                    mensaje = (
                                        'Operación fallida. Ya existe un usuario\n' +
                                        'registrado con este número telefónico.'
                                    )
                                    tipo_mensaje = 'error'
                            else:
                                mensaje = (
                                    'Operación fallida. Ya existe un usuario\n' +
                                    'registrado con este correo electrónico.'
                                )
                                tipo_mensaje = 'error'
                        else:
                            mensaje = (
                                'Operación fallida. Ya existe un usuario\n' +
                                'registrado con esta cedula.'
                            )
                            tipo_mensaje = 'error'
                    else:
                        mensaje = (
                            'Operación fallida. La pesona con esta cédula\n' +
                            'está registrado como un paciente.'
                        )
                        tipo_mensaje = 'error'
                else:
                    mensaje = 'Operación fallida. La cédula no es válida.'
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
        return redirect('/administracion/usuarios')

def editar_usuario(request, _id):
    try:
        if request.session['usuario_autenticado'] is not None:
            html = loader.get_template('monitor/editar-usuario.html')
            mensaje = ''
            tipo_mensaje = ''
            usuario = Usuario.objects.select_related().get(id=_id)
            if request.method == 'POST':
                cedula = request.POST.get('cedula', '')
                if es_cedula_valida(cedula):
                    pacientes = Paciente.objects.filter(persona__cedula=cedula)
                    if len(pacientes) == 0:
                        usuarios = Usuario.objects.filter(
                            persona__cedula=cedula
                        ).exclude(
                            id=usuario.id
                        )
                        if len(usuarios) == 0:
                            _correo = request.POST.get('correo', '')
                            usuarios = Usuario.objects.filter(
                                correo=_correo
                            ).exclude(
                                id=usuario.id
                            )
                            if len(usuarios) == 0:
                                _telefono = request.POST.get('telefono', '')
                                usuarios = Usuario.objects.filter(
                                    telefono=_telefono
                                ).exclude(
                                    id=usuario.id
                                )
                                if len(usuarios) == 0:
                                    persona = usuario.persona
                                    persona.cedula = cedula
                                    persona.nombre = request.POST.get('nombre', '')
                                    persona.apellido = request.POST.get('apellido', '')
                                    persona.save()
                                    usuario.correo = _correo
                                    usuario.telefono = _telefono
                                    usuario.clave = request.POST.get('clave', '')
                                    usuario.tipo = request.POST.get('tipo', '')
                                    usuario.save()
                                    mensaje = 'Operación exitosa. Usuario editado correctamente.'
                                    tipo_mensaje = 'exito'
                                else:
                                    mensaje = (
                                        'Operación fallida. Ya existe un usuario\n' +
                                        'registrado con este número telefónico.'
                                    )
                                    tipo_mensaje = 'error'
                            else:
                                mensaje = (
                                    'Operación fallida. Ya existe un usuario\n' +
                                    'registrado con este correo electrónico.'
                                )
                                tipo_mensaje = 'error'
                        else:
                            mensaje = (
                                'Operación fallida. Ya existe un usuario\n' +
                                'registrado con esta cedula.'
                            )
                            tipo_mensaje = 'error'
                    else:
                        mensaje = (
                            'Operación fallida. La persona con esta cédula\n' +
                            'está registrada como un paciente.'
                        )
                        tipo_mensaje = 'error'
                else:
                    mensaje = 'Operación fallida. La cédula no es válida.'
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
    except Exception:
        return redirect('/administracion/usuarios')

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
        return redirect('/administracion/usuarios')

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
    except Exception:
        return redirect('/administracion/pacientes')

def agregar_paciente(request):
    try:
        if request.session['usuario_autenticado'] is not None:
            html = loader.get_template('monitor/agregar-paciente.html')
            mensaje = ''
            tipo_mensaje = ''
            if request.method == 'POST':
                cedula_paciente = request.POST.get('cedula-paciente', '')
                if es_cedula_valida(cedula_paciente):
                    usuarios = Usuario.objects.filter(persona__cedula=cedula_paciente)
                    if len(usuarios) == 0:
                        pacientes = Paciente .objects.filter(persona__cedula=cedula_paciente)
                        if len(pacientes) == 0:
                            cedula_familiar = request.POST.get('cedula-familiar', '')
                            if es_cedula_valida(cedula_familiar):
                                familiares = Usuario.objects.filter(persona__cedula=cedula_familiar)
                                if len(familiares) > 0:
                                    _persona = Persona(
                                        cedula=cedula_paciente,
                                        nombre=request.POST.get('nombre', ''),
                                        apellido=request.POST.get('apellido', '')
                                    )
                                    _persona.save()
                                    contacto = Contacto(
                                        familiar=familiares[0],
                                        paciente=_persona
                                    )
                                    contacto.save()
                                    mensaje = 'Operación exitosa. Paciente registrado correctamente.'
                                    tipo_mensaje = 'exito'
                                else:
                                    mensaje = (
                                        'Operación fallida. El contacto con la cédula especificada\n' +
                                        'no se encuenta registrada como un enfermero/enfermera/familiar.'
                                    )
                                    tipo_mensaje = 'error'
                            else:
                                mensaje = 'Operación fallida. La cédula del contacto no es válida.'
                                tipo_mensaje = 'error'
                        else:
                            mensaje = (
                                'Operación fallida. Una persona con esta cédula ya se\n' +
                                'encuenta registrada como un paciente.'
                            )
                            tipo_mensaje = 'error'
                    else:
                        mensaje = (
                            'Operación fallida. Una persona con esta cédula ya se\n' +
                            'encuentra registrada como un enfermero/enfermera/familiar.'
                        )
                        tipo_mensaje = 'error'
                else:
                    mensaje = 'Operación fallida. La cédula del paciente no es válida.'
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
        return redirect('/administracion/pacientes')

def editar_paciente(request, _id):
    try:
        if request.session['usuario_autenticado'] is not None:
            html = loader.get_template('monitor/editar-paciente.html')
            mensaje = ''
            tipo_mensaje = ''
            paciente = Paciente.objects.select_related().get(id=_id)
            contacto = Contacto.objects.select_related().get(paciente__id=_id)
            if request.method == 'POST':
                cedula_paciente = request.POST.get('cedula-paciente', '')
                if es_cedula_valida(cedula_paciente):
                    cedula_familiar = request.POST.get('cedula-familiar', '')
                    if es_cedula_valida(cedula_familiar):
                        usuarios = Usuario.objects.filter(persona__cedula=cedula_paciente)
                        if len(usuarios) == 0:
                            pacientes = Paciente.objects.filter(
                                persona__cedula=cedula_paciente
                            ).exclude(id=paciente.id)
                            if len(pacientes) == 0:
                                paciente.cedula = cedula_paciente
                                paciente.nombre = request.POST.get('nombre', '')
                                paciente.apellido = request.POST.get('apellido', '')
                                paciente.fecha_nacimiento = request.POST.get('fecha-nacimiento', '')
                                paciente.save()
                                if cedula_familiar != contacto.familiar.persona.cedula:
                                    familiares = Usuario.objects.filter(
                                        persona__cedula=cedula_familiar
                                    ).exclude(id=contacto.familiar.id)
                                    if len(familiares) > 0:
                                        contacto.familiar = Usuario.objects.get(persona__cedula=cedula_familiar)
                                        contacto.save()
                                        mensaje = 'Operación exitosa. Paciente editado correctamente.'
                                        tipo_mensaje = 'exito'
                                    else:
                                        mensaje = (
                                            'Operación fallida. El contacto con la cédula especificada\n' +
                                            'no se encuenta registrada como un enfermero/enfermera/familiar.'
                                        )
                                        tipo_mensaje = 'error'
                                else:
                                    mensaje = 'Operación exitosa. Paciente editado correctamente.'
                                    tipo_mensaje = 'exito'
                            else:
                                mensaje = (
                                    'Operación fallida. Una persona con esta cédula ya se\n' +
                                    'encuenta registrada como un paciente.'
                                )
                                tipo_mensaje = 'error'
                        else:
                            mensaje = (
                                'Operación fallida. Una persona con esta cédula ya se\n' +
                                'encuentra registrada como un enfermero/enfermera/familiar.'
                            )
                            tipo_mensaje = 'error'
                    else:
                        mensaje = 'Operación fallida. La cédula del paciente no es válida.'
                        tipo_mensaje = 'error'
                else:
                    mensaje = 'Operación fallida. La cédula del paciente no es válida.'
                    tipo_mensaje = 'error'
            contexto = {
                'usuario_autenticado': request.session['usuario_autenticado'],
                'paciente': paciente,
                'contacto': contacto,
                'mensaje': mensaje,
                'tipo_mensaje': tipo_mensaje
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception as e:
        return redirect('/administracion/pacientes')

def eliminar_paciente(request, _id):
    try:
        if request.session['usuario_autenticado'] is not None:
            paciente = Paciente.objects.get(id=_id)
            paciente.delete()
            return redirect('/administracion/pacientes')
        else:
            return redirect('/')
    except Exception:
        return redirect('/administracion/pacientes')

def ver_imagen(request):
    try:
        if request.session['usuario_autenticado'] is not None:
            html = loader.get_template('monitor/ver-imagen.html')
            url = request.POST.get('url', '')
            contexto = {
                'imagen': url
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception:
        return redirect('/administracion/usuarios')
