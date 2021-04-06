from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    cedula = serializers.CharField(max_length=10)
    clave = serializers.CharField(max_length=15)
