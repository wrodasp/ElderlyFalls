from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializadores import CaidaSerializer
from .views import validar_credenciales
from .models import Caida

class LoginService(APIView):

    def get(self, request):
        try:
            cedula = request.query_params.get('cedula')
            clave = request.query_params.get('clave')
            resultado = {
                'resultado': validar_credenciales(cedula, clave)
            }
            return Response(resultado, content_type='text/plain')
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CaidaService(APIView):

    def get(self, request):
        try:
            caidas = Caida.objects.select_related().all()
            serializer = CaidaSerializer(caidas, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
