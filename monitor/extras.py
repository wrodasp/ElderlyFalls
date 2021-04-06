from .models import Persona, Usuario

def validar_usuario(_cedula, clave):
    personas = Persona.objects.filter(cedula=_cedula)
    if len(personas) > 0:
        usuario = Usuario.objects.filter(persona=personas[0])[0]
        return clave == usuario.clave
    else:
        return None
