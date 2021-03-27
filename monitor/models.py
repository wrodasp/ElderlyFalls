from django.db import models

# Create your models here.
class Caida(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    ubicacion = models.TextField(max_length=255)
    imagen = models.ImageField(upload_to='caidas/')

    def __str__(self):
        return f'Fecha={self.fecha} | Ubicacion={self.ubicacion}'
