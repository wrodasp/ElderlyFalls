from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Caida
from .extras import validar_usuario

# Create your views here.
def login(request):
    html = loader.get_template('monitor/login.html')
    mensaje = ''
    tipo_mensaje = ''
    if request.method == 'POST':
        _cedula = request.POST.get('cedula', '')
        clave = request.POST.get('clave', '')
        usuario_valido = validar_usuario(_cedula, clave)
        try:
            if usuario_valido:
                request.session['esta_logueado'] = True
                return redirect('administracion/')
            else:
                mensaje = 'La contraseña es incorrecta'
                tipo_mensaje = 'advertencia'
        except Exception:
            mensaje = f'El usuario {_cedula} no existe'
            tipo_mensaje = 'error'
    else:
        try:
            if request.session['esta_logueado']:
                return redirect('administracion/')
        except Exception:
            request.session['esta_logueado'] = False
    contexto = {
        'mensaje': mensaje,
        'tipo_mensaje': tipo_mensaje
    }
    return HttpResponse(html.render(contexto, request))

def logout(request):
    del request.session['esta_logueado']
    return redirect('/')

def administracion(request):
    try:
        if request.session['esta_logueado']:
            html = loader.get_template('monitor/administrador.html')
            caidas = Caida.objects.all().order_by('id')
            contexto = {
                'caidas': caidas,
                'tabla_vacia': range(10)
            }
            return HttpResponse(html.render(contexto, request))
        else:
            return redirect('/')
    except Exception:
        return redirect('/')
