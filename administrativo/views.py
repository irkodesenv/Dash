from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services.volumetria_athenas import VolumetriaAthenas
from conexoes.services.firebird import Conexao
from accounts.services.cliente import Cliente
from accounts.services.utils.clienteService import ClienteService


@login_required(redirect_field_name='login')
def retorna_volumetria_consumo_cliente(request):
    conexao = Conexao()
    
    cliente = request.POST.get("cliente")
    pick_realizado = request.POST.get("pick_realizado").split(" - ")
    pick_comparativo = request.POST.get("pick_comparativo").split(" - ")
    demonstracao = request.POST.get("demonstracao")
    descendentes = request.POST.get("descendentes")
    
    
    print(pick_realizado)
    
    data_ini = '2024-08-11'
    data_fim = '2024-09-10'
    codigo_empresa = []
    
    # Cadastro de clientes
    clientes = ClienteService(conexao)    
    lista_clientes = clientes.obter_clientes_formatados_formulario()
    
    # Volumetria 
    volumetria = VolumetriaAthenas(conexao, codigo_empresa = codigo_empresa, data_ini = data_ini, data_fim = data_fim)    
    data = volumetria.controllerMetricas()
    
    return render(request, 'dashboards/volumetria_cliente.html', {"clientes": lista_clientes, "data": data})
