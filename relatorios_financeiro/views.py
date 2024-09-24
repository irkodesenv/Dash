from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pprint import pprint 
from django.http import JsonResponse
from .services.relatorios_irko import RelatorioIrkoService
from .services.relatorios_athenas import RelatorioAthenasService
from clientes.services.controller_irko import ControllerClienteIrko
from clientes.services.controller_athenas import ControllerClienteAthenas
import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from django.conf import settings
from .utils.utils import combinar_dados_nexxcera, combinar_dados_bancos

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

    #Clientes 
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
    file_path = 'C:\\Users\\dcesar4152\\Desktop\\recorrencia.xlsx'  # Caminho do arquivo
    df = pd.read_excel(file_path)
    
    # Converter a coluna de vencimento para datetime e extrair o dia do vencimento
    if 'VENCIMENTO' in df.columns:
        df['VENCIMENTO'] = pd.to_datetime(df['VENCIMENTO'], errors='coerce')
        df['DiaDoVencimento'] = df['VENCIMENTO'].dt.day  # Extrair o dia do mês
    else:
        return render(request, 'relatorio_financeiro/relatorios/recorrencia.html', {
            'erro': 'A coluna VENCIMENTO não foi encontrada no arquivo Excel'
        })
    
    # Função para calcular o dia de vencimento mais frequente (moda)
    def calcular_dia_padrao(grupo):
        return grupo
        # Calcular o dia de vencimento mais frequente para o grupo (cliente + fornecedor)
        try:
            moda_dia = grupo['DiaDoVencimento'].mode()

            return moda_dia[0] if not moda_dia.empty else None
        except Exception as e:
            print(e)


    # Agrupar por CLIENTE e FORNECEDOR e calcular a moda do DiaDoVencimento
    df['DiaPadrao'] = df.groupby(['CLIENTE', 'FORNECEDOR'])['DiaDoVencimento'].transform(calcular_dia_padrao)

    moda_dia = df['DiaDoVencimento'].mode()
    df['DiaPadrao'] = moda_dia[0]

    # Definir a data de hoje
    hoje = datetime.today()

    # Função para calcular o próximo pagamento com base no DiaPadrao
    def calcular_proxima_previsao(row):
        dia_padrao = row['DiaPadrao']
        if pd.isnull(dia_padrao):
            return None
        
        # Se o dia atual é menor ou igual ao DiaPadrao, o próximo pagamento é este mês
        if hoje.day <= dia_padrao:
            return datetime(hoje.year, hoje.month, int(dia_padrao))
        else:
            # Caso contrário, o próximo pagamento será no mês seguinte
            proximo_mes = hoje + timedelta(days=30)  # Ajuste para o próximo mês
            return datetime(proximo_mes.year, proximo_mes.month, int(dia_padrao))

    # Calcular a próxima previsão de pagamento para cada linha
    df['ProximaPrevisao'] = df.apply(calcular_proxima_previsao, axis=1)

    # Filtrar os pagamentos que ocorrem nos próximos 7 dias
    proximos_7_dias = hoje + timedelta(days=7)
    df_proximos_7_dias = df[(df['ProximaPrevisao'] >= hoje) & (df['ProximaPrevisao'] <= proximos_7_dias)]

    # Contar o número de fornecedores nos próximos 7 dias
    contagem_fornecedores_proximos_7_dias = df_proximos_7_dias.groupby(['CLIENTE', 'FORNECEDOR']).size()

    # Selecionar as colunas relevantes para o painel
    df_painel = df_proximos_7_dias[['CLIENTE', 'FORNECEDOR', 'ProximaPrevisao']]

    # Preparar os dados para o template
    context = {
        'df_painel': df_painel.to_dict(orient='records'),  # Transformar o DataFrame em uma lista de dicionários
        'contagem_fornecedores': contagem_fornecedores_proximos_7_dias.to_dict(),  # Contagem de fornecedores
        'data': df.to_dict(orient='records')
    }
    
    # Renderizar o template com os dados
    return render(request, 'relatorios_financeiro/relatorios/recorrencia.html', context)


def serializer_df(df):
    print(df)