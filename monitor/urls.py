from django.urls import path
from . import servicios
from . import views

urlpatterns = [
    #Vistas
    path('', views.login),
    path('logout/', views.logout),
    path('administracion/', views.administracion),
    path('administracion/usuarios', views.usuarios),
    path('administracion/usuarios/agregar', views.agregar_usuario),
    path('administracion/usuarios/editar/<int:_id>', views.editar_usuario),
    path('administracion/usuarios/eliminar/<int:_id>', views.eliminar_usuario),
    path('administracion/pacientes', views.pacientes),
    path('administracion/pacientes/agregar', views.agregar_paciente),
    path('administracion/pacientes/editar/<int:_id>', views.editar_paciente),
    path('administracion/pacientes/eliminar/<int:_id>', views.eliminar_paciente),
    #API REST
    path('rest/validar-usuario', servicios.LoginService.as_view()),
    path('rest/caidas', servicios.CaidaService.as_view())
]
