from rest_framework import serializers
from .models import Persona, Paciente, Caida

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('id', 'cedula', 'nombre', 'apellido')

class PacienteSerializer(serializers.ModelSerializer):

    persona = PersonaSerializer(many=False)

    class Meta:
        model = Paciente
        fields = ('id',  'persona', 'fecha_nacimiento')

    def create(self, validated_data):
        persona_validated_data = validated_data.pop('persona')
        paciente = Paciente.objects.create(**validated_data)
        persona_serializer = self.fields['persona']
        persona_validated_data['paciente'] = paciente
        persona = persona_serializer.create(persona_validated_data)
        return paciente

class CaidaSerializer(serializers.ModelSerializer):

    paciente = PacienteSerializer(many=False)

    class Meta:
        model = Caida
        fields = ('id', 'fecha', 'precision', 'imagen', 'paciente', 'revisado')

    def create(self, validated_data):
        paciente_validated_data = validated_data.pop('paciente')
        caidas = Caida.objects.create(**validated_data)
        paciente_serializer = self.fields['paciente']
        paciente_validated_data['caidas'] = caidas
        paciente = paciente_serializer.create(paciente_validated_data)
        return caidas
