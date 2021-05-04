from django.core.files import File
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializadores import CaidaSerializer
from .views import validar_credenciales
from .models import Caida, Contacto, Paciente
from datetime import datetime
import base64

class LoginService(APIView):

    def get(self, request):
        try:
            cedula = request.query_params.get('cedula')
            clave = request.query_params.get('clave')
            resultado = validar_credenciales(cedula, clave)
            return Response(resultado, content_type='text/plain')
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CaidaService(APIView):

    def get(self, request):
        try:
            familiar_id = request.query_params.get('id')
            data = []
            if familiar_id is not None:
                contactos = Contacto.objects.select_related().filter(familiar__id=familiar_id)
                for contacto in contactos:
                    caidas = contacto.paciente.caida_set.all()
                    for caida in caidas:
                        data.append(caida)
            else:
                data = Caida.objects.select_related().all()
            serializer = CaidaSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            _fecha = datetime.now()
            _imagen = open('imagen', 'wb')
            _imagen.write(base64.b64decode((request.data.get('imgbinary'))))
            _imagen.close()
            _imagen = open('imagen', 'rb')
            _precision = request.data.get('precision')
            _paciente = Paciente.objects.all()[0]
            caida = Caida(
                fecha=_fecha,
                precision=_precision,
                paciente=_paciente
            )
            caida.imagen.save(str(_fecha), File(_imagen))
            _imagen.close()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
