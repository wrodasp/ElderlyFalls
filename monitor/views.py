from django.http import HttpResponse
from django.template import loader
from .models import Caida

# Create your views here.
def go_index(request):
    caidas = Caida.objects.order_by('id')
    html = loader.get_template('monitor/index.html')
    contexto = {
        'caidas': caidas,
        'tabla_vacia': range(10)
    }
    return HttpResponse(html.render(contexto, request))
