from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services.volumetria_athenas import VolumetriaAthenas
from conexoes.services.firebird import Conexao
from accounts.services.cliente import Cliente
from accounts.services.utils.clienteService import ClienteService
from utils.views import converte_array_data_para_sistema


@login_required(redirect_field_name='login')
def retorna_volumetria_consumo_cliente(request):
    conexao = Conexao()
    
    # Cadastro de clientes
    clientes = ClienteService(conexao)    
    lista_clientes = clientes.obter_clientes_formatados_formulario()
    
    cliente = request.POST.get("cliente")
    pick_realizado = converte_array_data_para_sistema(request.POST.get("pick_realizado").split(" - "))
    pick_comparativo = converte_array_data_para_sistema(request.POST.get("pick_comparativo").split(" - "))
    demonstracao = request.POST.get("demonstracao")
    descendentes = request.POST.get("descendentes")   
    
    data_ini = pick_realizado[0]
    data_fim = pick_realizado[1]
    
    data_comparativo_ini = pick_comparativo[0]
    data_comparativo_fim = pick_comparativo[1]
    codigo_empresa = []
    
    # Volumetria 
    volumetria = VolumetriaAthenas(conexao, codigo_empresa = codigo_empresa, data_ini = data_ini, data_fim = data_fim, data_comparativo_ini = data_comparativo_ini, data_comparativo_fim = data_comparativo_fim)    
    data = volumetria.controllerMetricas()
    
    return render(request, 'dashboards/volumetria_cliente.html', {"clientes": lista_clientes, "data": data})
