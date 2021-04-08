from django.db import models

# Create your models here.
class Caida(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    ubicacion = models.TextField(max_length=255)
    imagen = models.ImageField(upload_to='caidas/')

    def __str__(self):
        return f'{self.pk} -> {self.fecha} | {self.ubicacion}'

class Persona(models.Model):
    cedula = models.TextField(max_length=10, unique=True)
    nombre = models.TextField(max_length=50)
    apellido = models.TextField(max_length=50)
    
    def __str__(self):
        return f'{self.cedula} -> {self.nombre}  {self.apellido}'

class Usuario(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    clave = models.TextField(max_length=30)
    tipo = models.TextField(max_length=10, default='regular')

    def __str__(self):
        return f'{self.persona.__str__()} | {self.tipo}'

class Contacto(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    telefono = models.TextField(max_length=10)

    def __str__(self):
        return f'{self.persona.__str__()} | {self.telefono}'
