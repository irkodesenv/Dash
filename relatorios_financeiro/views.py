from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pprint import pprint 
from django.http import JsonResponse
from .services.relatorios_irko import RelatorioIrkoService
from .services.relatorios_athenas import RelatorioAthenasService
from clientes.services.controller_irko import ControllerClienteIrko
from clientes.services.controller_athenas import ControllerClienteAthenas
from conexoes.services.firebird import Conexao
from accounts.services.utils.clienteService import ClienteService
import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from django.conf import settings
from .utils.utils import combinar_dados_nexxcera, combinar_dados_bancos
from central.settings import BASE_DIR, STATIC_URL

logger = logging.getLogger(__name__)

@login_required(redirect_field_name='login')
def retorna_relatorio_financeiro(request):
    
    # Se for uma solicitação Formulario
    if request.method == 'POST':
        filtros = request.POST  
        request.session['filtros'] = filtros

        return redirect('relatorios_financeiro:rel_financeiro')
    
    filtros = request.session.get('filtros', {})
    
    codigo_cliente = filtros.get('select-clientes', []) 

    # Clientes 
    clientes_irko = processa_clientes_irko([])
    clientes_athenas = processa_clientes_athenas("")

    clientes = combina_clientes(clientes_irko, clientes_athenas)

    # Nexxera
    dados_nexxcera_irko = processa_relatorio_empresas_nexxera_irko([codigo_cliente])
    dados_nexxcera_athenas = processa_relatorio_empresas_nexxera_athenas(codigo_cliente)

    if dados_nexxcera_irko['success'] and dados_nexxcera_athenas['success']:
        dados_nexxcera_combinado = combinar_dados_nexxcera(dados_nexxcera_athenas, dados_nexxcera_irko)
    else:
        dados_nexxcera_combinado = {'success': False, 'code': 404, 'data': 'Erro ao chamar API'}

    # Operadores Irko
    dados_operadores = processsa_dados_operadores_irko([codigo_cliente])

    # Bancos
    dados_bancos_athenas = processa_grafico_bancos_athenas(codigo_cliente)
    dados_bancos_irko = processa_grafico_bancos_irko([codigo_cliente])

    combinar_dados_bancos(dados_bancos_irko, dados_bancos_athenas)
    dados_bancos_combinados_ordenados = dict(sorted(dados_bancos_irko['lista_bancos'].items(), key=lambda x: x[1]['qtd_contas'], reverse=True))

    request.session['filtros'] = {}
    return render(request, 'relatorios_financeiro/relatorio_financeiro.html', 
                { 
                   "dados_athenas": dados_nexxcera_combinado, 
                   "dados_operadores": dados_operadores['operadores'], 
                   "contagem_operadores_inteiro": dados_operadores['contagem_inteiro'], 
                   'dados_operadores_porcentagem': dados_operadores['contagem_porcentagem'],
                   'lista_bancos': dados_bancos_combinados_ordenados,
                   'ranking_bancos': json.dumps(dados_bancos_irko['ranking_bancos']),
                   'clientes': clientes,
                   'filtro_cliente': codigo_cliente
                })


def processa_relatorio_empresas_nexxera_irko(arr_clientes):
    try:
        relatorio_service = RelatorioIrkoService(arr_clientes = arr_clientes)    
        return relatorio_service.empresas_nexxcera()
    except Exception as e:        
        #logger.error(f"Erro ao processar relatório: {str(e)}")
        return {'data': {'code': 500, 'message': 'Não foi possível retornar dados.'}, 'success': False}


def processa_relatorio_empresas_nexxera_athenas(arr_clientes):
    try:
        relatorio_service = RelatorioAthenasService(arr_clientes = arr_clientes)    
        return relatorio_service.empresas_nexxcera()
    except Exception as e:       
        #logger.error(f"Erro ao processar relatório: {str(e)}")
        return {
            'success': False,
            'code': 500,
            'data': 'Não foi possível retornar nexxcera do Athenas'
        }


def processsa_dados_operadores_irko(arr_clientes):
    try:
        relatorio_service = RelatorioIrkoService(arr_clientes = arr_clientes) 
        return relatorio_service.dados_operadores()   
    except Exception as e:
        return {'data': {'code': 500, 'message': 'Não foi possível retornar dados.'}, 'success': False}


def processa_grafico_bancos_irko(arr_clientes):
    try:
        relatorio_service = RelatorioIrkoService(arr_clientes = arr_clientes) 
        return relatorio_service.bancos()   
    except Exception as e:
        return {'data': {'code': 500, 'message': 'Não foi possível retornar dados.'}, 'success': False}


def processa_grafico_bancos_athenas(arr_clientes):
    try:
        relatorio_service = RelatorioAthenasService(arr_clientes = arr_clientes)    
        return relatorio_service.ranking_bancos()
    except Exception as e:  
        #logger.error(f"Erro ao processar relatório: {str(e)}")
        return {
            'success': False,
            'code': 500,
            'data': 'Não foi possível retornar bancos do Athenas'
        }
    

def processa_clientes_irko(arr_clientes):
    try:
        clientes = ControllerClienteIrko(arr_clientes = arr_clientes)    
        return clientes.retorna_cadastro_clientes()
    except Exception as e:  
        #logger.error(f"Erro ao processar relatório: {str(e)}")
        return {
            'success': False,
            'code': 500,
            'data': 'Não foi possível retornar clientes do Irko'
        }
    

def processa_clientes_athenas(arr_clientes):
    try:
        clientes = ControllerClienteAthenas(arr_clientes = arr_clientes)
        dados_clientes = clientes.retorna_cadastro_clientes()  

        return {
            'success': True,
            'code': 200,
            'data': {'ListaEmpresas': dados_clientes}
        }
    except Exception as e:  
        return {
            'success': False,
            'code': 500,
            'data': 'Não foi possível retornar clientes do Athenas'
        }
    

def combina_clientes(clientes_irko, clientes_athenas):

    # Verifica se ambas as respostas foram bem-sucedidas
    if not (clientes_irko['success'] and clientes_athenas['success']):
        return {'success': False, 'code': 500, 'data': {'message': 'Erro ao processar os dados.'}}

    lista_empresas_irko = clientes_irko.get('data', {}).get('ListaEmpresas', [])
    lista_empresas_athenas = clientes_athenas.get('data', {}).get('ListaEmpresas', [])

    # Merge das duas listas
    lista_empresas_combinada = lista_empresas_irko + lista_empresas_athenas

    # Ordena a lista combinada pelo campo 'Codigo'
    lista_empresas_combinada.sort(key=lambda empresa: int(empresa.get('Codigo', 0)))

    return {
        'success': True,
        'code': 200,
        'data': {'ListaEmpresas': lista_empresas_combinada}
    }


def retorna_operadores(request):
    codigo_cliente = request.POST.get('codigo_cliente', "")
    codigo_operador = request.POST.get('codigo', "")

    dados_operadores = processsa_dados_operadores_irko([codigo_cliente])

    try:
        if codigo_operador:
            for operador in dados_operadores['operadores']:    
                if operador['id_usuario'] == codigo_operador:
                    return JsonResponse([operador], safe=False)

        return JsonResponse(dados_operadores['operadores'], safe=False)
    except Exception as e:
        return JsonResponse(dados_operadores['operadores'], safe=False)
    

def retorna_recorrencia(request):
    # Carregar o arquivo Excel
    file_path = f'{BASE_DIR}/{STATIC_URL}/media/consumiveis/recorrencia.xlsx'  # Caminho do arquivo
    df = pd.read_excel(file_path)

    # Certifique-se de que a coluna 'VENCIMENTO' está sendo corretamente convertida para o formato datetime (somente data)
    df['VENCIMENTO'] = pd.to_datetime(df['VENCIMENTO'], errors='coerce').dt.date

    # Remover quaisquer valores de vencimento inválidos (valores que não foram convertidos)
    df = df.dropna(subset=['VENCIMENTO'])

    # Simular o cálculo de recorrência mensal
    hoje = datetime.today().date()
    data_futura = hoje + timedelta(days=7)

    # Lista para armazenar previsões de pagamentos
    pagamentos = []

    # Filtro de clientes
    conexao = Conexao()
    
    # Cadastro de clientes
    clientes = ClienteService(conexao)    
    lista_clientes = clientes.obter_clientes_formatados_formulario()

    # Obter o cliente selecionado da requisição
    cliente_selecionado = request.POST.get('select-clientes')

    if cliente_selecionado:
        # Filtrar o DataFrame pelo cliente selecionado
        df = df[df['CLIENTE'] == cliente_selecionado]

    # Agrupar por fornecedor e calcular recorrências
    fornecedores = df.groupby('FORNECEDOR')
    
    for fornecedor, grupo in fornecedores:
        # Obter o último vencimento registrado
        ultimo_vencimento = grupo['VENCIMENTO'].max()

        # Verificar se o último vencimento é uma data válida
        if ultimo_vencimento:
            # Supondo recorrência mensal, o próximo vencimento será no mesmo dia no próximo mês
            proximo_vencimento = ultimo_vencimento + timedelta(days=30)

            # Se o próximo vencimento estiver dentro dos próximos 7 dias, adicionar à lista
            if hoje <= proximo_vencimento <= data_futura:
                
                # Obter o último pagamento e tratar se for NaT (não pago)
                ultimo_pagto = grupo['PAGTO'].max()
                if pd.isna(ultimo_pagto):
                    ultimo_pagto_str = 'Não pago'
                else:
                    ultimo_pagto_str = ultimo_pagto.strftime('%d/%m/%Y')
                
                qtd_doctos = grupo.shape[0]

                pagamentos.append({
                    'cliente': grupo['CLIENTE'].iloc[0],  # Assume-se que todos os registros no grupo tenham o mesmo cliente
                    'fornecedor': fornecedor,
                    'data_previsao': proximo_vencimento.strftime('%d/%m/%Y'),
                    'ultimo_pagto': ultimo_pagto.strftime('%d/%m/%Y') if pd.notna(ultimo_pagto) else 'Não pago',
                    'qtd_doctos': qtd_doctos
                })
    
    # Substituir valores nulos na coluna 'cliente' por strings vazias para evitar erro de comparação
    for pagamento in pagamentos:
        if not isinstance(pagamento['cliente'], str):
            pagamento['cliente'] = 'Cliente não identificado'

    # Ordenar a lista de pagamentos por ordem alfabética pelo nome do cliente
    pagamentos = sorted(pagamentos, key=lambda x: x['cliente'])

    # Verifique o conteúdo da lista de pagamentos
    context = {
        'pagamentos': pagamentos,
        'clientes' : lista_clientes,
        'cliente_selecionado': cliente_selecionado,
    }
    
    return render(request, 'relatorios_financeiro/relatorios/recorrencia.html', context)