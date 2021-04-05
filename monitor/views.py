from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Caida, Usuario

# Create your views here.
def iniciar_sesion(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario', '')
        clave = request.POST.get('clave', '')
        #usuario_consultado = Usuario.objects.filter(persona=usuario)
        usuario_consultado = '0000000000'
        #if clave == usuario_consultado.clave:
        if clave == '123456789':
            html = loader.get_template('monitor/administrador.html')
            request.session['esta_logueado'] = True
            caidas = Caida.objects.all().order_by('id')
            contexto = {
                'caidas': caidas,
                'tabla_vacia': range(10)
            }
            return HttpResponse(html.render(contexto, request))
        else:
            html = loader.get_template('monitor/login.html')
            request.session['esta_logueado'] = False
            return HttpResponse(html.render({}, request))
    else:
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
                html = loader.get_template('monitor/login.html')
                request.session['esta_logueado'] = False
                return HttpResponse(html.render({}, request))
        except Exception as e:
            html = loader.get_template('monitor/login.html')
            request.session['esta_logueado'] = False
            return HttpResponse(html.render({}, request))

def cerrar_sesion(request):
    html = loader.get_template('monitor/login.html')
    del request.session['esta_logueado']
    return redirect('/')
