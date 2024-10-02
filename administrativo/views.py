from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services.volumetria_athenas import VolumetriaAthenas
from conexoes.services.firebird import Conexao
from accounts.services.cliente import Cliente
from accounts.services.utils.clienteService import ClienteService
from utils.views import converte_array_data_para_sistema
from django.http import JsonResponse


@login_required(redirect_field_name='login')
def retorna_volumetria_consumo_cliente(request):
    conexao = Conexao()
    
    # Cadastro de clientes
    clientes = ClienteService(conexao)    
    lista_clientes = clientes.obter_clientes_formatados_formulario()
    
    cliente = request.POST.get("cliente")
    demonstracao = int(request.POST.get("demonstracao")) if request.POST.get("demonstracao") else 1
    descendentes = request.POST.get("descendentes") 
    
    if request.POST:    

        pick_realizado = converte_array_data_para_sistema(request.POST.get("pick_realizado").split(" - "))
        pick_comparativo = converte_array_data_para_sistema(request.POST.get("pick_comparativo").split(" - "))
       
        filtros = {
            "pick_realizado": request.POST.get("pick_realizado"),
            "pick_comparativo": request.POST.get("pick_comparativo"),
            "cliente": int(cliente) if cliente else "",
            "descendentes": descendentes,  
            "demonstracao": demonstracao          
        }  
        
        data_ini = pick_realizado[0]
        data_fim = pick_realizado[1]
        
        data_comparativo_ini = pick_comparativo[0]
        data_comparativo_fim = pick_comparativo[1]
    else:
        filtros = {
            "pick_realizado": ['11/09/2024 - 10/10/2024'],
            "pick_comparativo": ['11/08/2024 - 10/09/2024']
        }  
        
        data_ini = "2024-09-11"
        data_fim = "2024-10-10"
        
        data_comparativo_ini = "2024-08-11"
        data_comparativo_fim = "2024-09-10"
            
    # Volumetria 
    volumetria = VolumetriaAthenas(conexao, codigo_empresa = cliente, data_ini = data_ini, data_fim = data_fim, data_comparativo_ini = data_comparativo_ini, data_comparativo_fim = data_comparativo_fim)    
    data = volumetria.controllerMetricas(demonstracao)
    
    return render(request, 'dashboards/volumetria_cliente.html', {"filtros": filtros, "clientes": lista_clientes, "data": data})


def filtro_volumetria(request):
    pass


def obter_descendentes(request):
    conexao = Conexao()
    clientes = ClienteService(conexao)  
    codigo_cliente = request.POST.get("cliente") 

    lista_descendentes = clientes.obter_descendentes(codigo_cliente)
    
    return JsonResponse(lista_descendentes, safe=False)   