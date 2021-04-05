from django.db import models

# Create your models here.
class Caida(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    ubicacion = models.TextField(max_length=255)
    imagen = models.ImageField(upload_to='caidas/')

class Persona(models.Model):
    cedula = models.TextField(max_length=10)
    nombre = models.TextField(max_length=50)
    apellido = models.TextField(max_length=50)

class Usuario(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    clave = models.TextField(max_length=15)

class Contacto(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    telefono = models.TextField(max_length=10)
