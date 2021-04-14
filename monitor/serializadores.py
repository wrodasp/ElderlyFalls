from rest_framework import serializers
from .models import Caida

class CaidaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Caida
        fields = ('id', 'fecha', 'presicion', 'imagen', 'paciente')
