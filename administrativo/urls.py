from django.urls import path
from . import views

app_name = 'administrativo'
urlpatterns = [
    #Dash de volumetria de consumo de Clientes
    path('volumetria/', views.retorna_volumetria_consumo_cliente, name="retornaVolumetriaConsumoCliente"),
]