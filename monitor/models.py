from django.db import models

# Create your models here.
class Caida(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    ubicacion = models.TextField(max_length=255)
    imagen = models.ImageField(upload_to='monitor/caidas')

    def __str__(self):
        return f'{self.pk} -> {self.fecha} | {self.ubicacion}'

    def __json__(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'ubicacion': self.ubicacion,
            'imagen': self.imagen
        }

class Persona(models.Model):
    cedula = models.TextField(max_length=10, unique=True)
    nombre = models.TextField(max_length=50)
    apellido = models.TextField(max_length=50)

    def __str__(self):
        return f'{self.cedula} -> {self.nombre}  {self.apellido}'

    def __json__(self):
        return {
            'id': self.id,
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido
        }

class Usuario(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    clave = models.TextField(max_length=30)
    tipo = models.TextField(max_length=10, default='regular')

    def __str__(self):
        return f'{self.persona.__str__()} | {self.tipo}'

    def __json__(self):
        return {
            'id': self.id,
            'clave': self.clave,
            'tipo': self.tipo,
            'persona': self.persona.__json__()
        }

class Contacto(models.Model):
    paciente = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name='contactos',
        default=None
    )
    familiar = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        default=None
    )
    telefono = models.TextField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.persona.__str__()} | {self.telefono}'

    def __json__(self):
        return {
            'id': self.id,
            'telefono': self.telefono,
            'paciente': self.paciente.__json__(),
            'familiar': self.familiar.__json__()
        }
