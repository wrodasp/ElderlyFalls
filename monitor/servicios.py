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
            print(e)
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
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            _fecha = datetime.now()
            _precision = request.data.get('precision')
            _paciente = Paciente.objects.all()[0]
            datos_imagen = base64.b64decode((request.data.get('imgbinary')))
            with open('imagen.aux', 'w+b') as _imagen:
                caida = Caida(
                    fecha=_fecha,
                    precision=_precision,
                    paciente=_paciente
                )
                _imagen.write(datos_imagen)
                caida.imagen.save(str(_fecha), File(_imagen))
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ImagenService(APIView):

    def get(self, request):
        try:
            _id = request.query_params.get('id')
            caida = Caida.objects.get(id=_id)
            imagen = open(caida.imagen.path, 'rb')
            data = base64.b64encode(imagen.read())
            imagen.close()
            return Response(data, content_type='text/plain')
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class RevisarCaidaService(APIView):

    def get(self, request):
        try:
            _id = request.query_params.get('id')
            caida = Caida.objects.get(id=_id)
            caida.revisado = True
            caida.save()
            serializer = CaidaSerializer(caida, many=False)
            return Response(serializer.data, content_type='text/plain')
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
