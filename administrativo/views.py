from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services.volumetria_athenas import VolumetriaAthenas
from conexoes.services.firebird import Conexao


@login_required(redirect_field_name='login')
def retorna_volumetria_consumo_cliente(request):
    
    data_ini = '2024-09-01'
    data_fim = '2024-09-30'
    codigo_empresa = []
    conexao = Conexao()
    
    obj = VolumetriaAthenas(conexao, codigo_empresa = codigo_empresa, data_ini = data_ini, data_fim = data_fim)
    
    data = obj.controllerMetricas()
    
    return render(request, 'dashboards/volumetria_cliente.html', {"data": data})
