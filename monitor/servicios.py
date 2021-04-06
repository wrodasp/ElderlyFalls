from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializadores import LoginSerializer
from .extras import validar_usuario

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            cedula = serializer.validated_data.get('cedula')
            clave = serializer.validated_data.get('clave')
            resultado = {
                'resultado': validar_usuario(cedula, clave)
            }
            return Response(resultado)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
