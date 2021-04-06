from django.urls import path
from . import servicios
from . import views

urlpatterns = [
    #Vistas
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('administracion/', views.administracion, name='administracion'),

    #API REST
    path('rest/validar-usuario', servicios.LoginView.as_view(), name='validar-usuario')
]
