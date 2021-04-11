from django.db import models

# Create your models here.
class Persona(models.Model):
    cedula = models.TextField(max_length=10, default='0000000000')
    nombre = models.TextField(max_length=50)
    apellido = models.TextField(max_length=50)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    def __json__(self):
        return {
            'id': self.id,
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido
        }

class Usuario(models.Model):
    correo = models.EmailField(max_length=255, default='')
    clave = models.TextField(max_length=30)
    tipo = models.TextField(max_length=10, default='regular')
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.correo} | {self.tipo}'

    def __json__(self):
        return {
            'id': self.id,
            'correo': self.correo,
            'clave': self.clave,
            'tipo': self.tipo,
            'persona': self.persona.__json__()
        }

class Paciente(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f'{self.persona.__json__()} | {self.fecha_nacimiento.strftime("%b %d %Y")}'

    def __json__(self):
        return {
            'id': self.id,
            'fecha-nacimiento': self.fecha_nacimiento,
            'persona': self.persona.__json__()
        }

class Contacto(models.Model):
    familiar = models.OneToOneField(Persona, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    telefono = models.TextField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.persona.__str__()} | {self.telefono}'

    def __json__(self):
        return {
            'id': self.id,
            'telefono': self.telefono,
            'familiar': self.familiar.__json__(),
            'paciente': self.paciente.__json__()
        }

class Caida(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    presicion = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    imagen = models.ImageField(upload_to='monitor/caidas')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.fecha.strftime("%b %d %Y %H:%M:%S")} | {self.ubicacion}'

    def __json__(self):
        return {
            'id': self.id,
            'fecha': self.fecha.strftime("%b %d %Y %H:%M:%S"),
            'presicion': self.presicion,
            'imagen': self.imagen,
            'paciente': self.paciente.__json__()
        }
