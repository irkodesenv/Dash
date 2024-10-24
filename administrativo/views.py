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
    
    filtros = {
        "pick_realizado": ['11/10/2024 - 10/11/2024'],
        "pick_comparativo": ['11/09/2024 - 10/10/2024']
    }  
        
    return render(request, 'dashboards/volumetria_cliente.html', {"filtros": filtros, "clientes": lista_clientes})


def processar_volumetria_athenas(request, controller_func):
    """
        Processa a volumetria baseada nos filtros fornecidos e chama o método de controle apropriado.

        Args:
            request (HttpRequest): Objeto de requisição HTTP.
            controller_func (str): Nome do método de controle a ser chamado em VolumetriaAthenas.

        Returns:
            JsonResponse: Resposta JSON contendo os dados processados ou mensagem de erro.
    """
    filtro = trata_filtro_volumetria(request)
    
    conexao = Conexao()
    
    volumetria = VolumetriaAthenas(
        conexao, 
        codigo_empresa=filtro['cliente'], 
        data_ini=filtro['data_realizado_ini'], 
        data_fim=filtro['data_realizado_fim'], 
        data_comparativo_ini=filtro['data_comparativo_ini'], 
        data_comparativo_fim=filtro['data_comparativo_fim'],
        filial=filtro['descendentes']
    )

    # Chama o método correspondente
    demonstracao = filtro['demonstracao']
    controller = getattr(volumetria, controller_func)
    dados = controller(demonstracao)
    
    return JsonResponse(dados)


def volumetria_folha(request):
    return processar_volumetria_athenas(request, 'controllerFolha')


def volumetria_financeiro(request):
    return processar_volumetria_athenas(request, 'controllerFinanceiro')


def volumetria_fiscal(request):
    return processar_volumetria_athenas(request, 'controllerFiscal')


def volumetria_contabil(request):
    return processar_volumetria_athenas(request, 'controllerContabil')


def obter_descendentes(request):
    conexao = Conexao()
    clientes = ClienteService(conexao)  
    codigo_cliente = request.POST.get("cliente") 

    lista_descendentes = clientes.obter_descendentes(codigo_cliente)
    
    return JsonResponse(lista_descendentes, safe=False)   


def trata_filtro_volumetria(request):
    pick_realizado = converte_array_data_para_sistema(request.POST.get("filtro[pick_realizado]").replace("['", "").replace("']", "").split(" - "))
    pick_comparativo = converte_array_data_para_sistema(request.POST.get("filtro[pick_comparativo]").replace("['", "").replace("']", "").split(" - "))

    return {
        "cliente": request.POST.get("filtro[cliente]"),
        "demonstracao": int(request.POST.get("filtro[demonstracao]")) if request.POST.get("filtro[demonstracao]") else 1,
        "descendentes": request.POST.get("filtro[descendentes]"),
        "data_realizado_ini": pick_realizado[0],
        "data_realizado_fim": pick_realizado[1],
        "data_comparativo_ini": pick_comparativo[0],
        "data_comparativo_fim": pick_comparativo[1]
    }