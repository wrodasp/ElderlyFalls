from django.urls import path
from . import servicios
from . import views

urlpatterns = [
    #Vistas
    path('', views.login),
    path('logout/', views.logout),
    path('administracion/', views.administracion),
    path('administracion/usuarios', views.usuarios),
    path('administracion/usuario/eliminar/<int:id>', views.eliminar_usuario),
    #API REST
    path('rest/validar-usuario', servicios.LoginView.as_view()),

]
