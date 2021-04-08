from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .views import validar_usuario

class LoginView(APIView):

    def get(self, request):
        try:
            cedula = request.query_params.get('cedula')
            clave = request.query_params.get('clave')
            resultado = {
                'resultado': validar_usuario(cedula, clave)
            }
            return Response(resultado)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
