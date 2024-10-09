from django.urls import path
from . import views

app_name = 'administrativo'
urlpatterns = [
    #Dash de volumetria de consumo de Clientes
    path('volumetria/', views.retorna_volumetria_consumo_cliente, name="retornaVolumetriaConsumoCliente"),
    path('obterDadosDescendentes/', views.obter_descendentes, name="obterDadosDescendentes"),
    path('volumetriaFolha', views.volumetria_folha, name="retornaVolumetriaFolha"),
    path('volumetriaFinanceiro', views.volumetria_financeiro, name="retornaVolumetriaFinanceiro"),
    path('volumetriaContabil', views.volumetria_contabil, name="retornaVolumetriaContabil")
]