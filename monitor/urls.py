from django.urls import path
from . import views

urlpatterns = [
    path('', views.iniciar_sesion, name='login'),
    path('cerrar_sesion/', views.cerrar_sesion, name='logout')
]
