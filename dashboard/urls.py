from django.urls import path
from django.contrib import admin
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.return_dashboard, name="dashboard"),
    path('retornaDadosDashboard/', views.retorna_dados_dashboard, name="retornaDadosDashboard"),
    path('retornaDadosDoctosIndefinidos/', views.retorna_dados_doctos_indefinidos, name="retornaDadosDoctosIndefinidos"),
    path('retornaDadosDoctosGerais/', views.retorna_dados_doctos_gerais, name="retornaDadosDoctosGerais"),
    path('retornaRankingDoctoIndefinido/', views.retorna_ranking_doctos_indefinidos, name="retornaRankingDoctoIndefinido"),
    #Dash de volumetria de consumo de Clientes
    path('retornaVolumetriaConsumoCliente/', views.retorna_volumetria_consumo_cliente, name="retornaVolumetriaConsumoCliente"),
]