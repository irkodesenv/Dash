from django.shortcuts import render
from pprint import pprint
from .services.financeiro_irko import FinanceiroIrko 
from .services.financeiro_athenas import FinanceiroAthenas
from .services.financeiro_athenas import Financeiro
from conexoes.services.firebird import Conexao
from conexoes.services.api import Api
import json


def retorna_relatorio_financeiro(request):

    # Athenas
    #dados_athenas = processa_relatorio_empresas_nexxera_athenas()

    # Irko
    dados_nexxera = processa_relatorio_empresas_nexxera_irko()
    
    # Provisorio
    dados_athenas = dados_nexxera
    dados_operadores = processsa_dados_operadores()

    dados_bancos = processa_grafico_bancos()

    return render(request, 'relatorios_financeiro/relatorio_financeiro.html', 
                  {"dados_nexxera": dados_nexxera, 
                   "dados_athenas": dados_athenas, 
                   "dados_operadores": dados_operadores['operadores'], 
                   "contagem_operadores_inteiro": dados_operadores['contagem_inteiro'], 
                   'dados_operadores_porcentagem': dados_operadores['contagem_porcentagem'],
                   'lista_bancos': dados_bancos['lista_bancos'],
                   'ranking_bancos': json.dumps(dados_bancos['ranking_bancos'] )
                   })


def processa_relatorio_empresas_nexxera_irko():
    api = Api(url = "http://diamante2:57773/csp/prgfnc/dash/EmpresasFinanceiro")
 
    financeiro_irko = FinanceiroIrko()
    financeiro_irko.dados = api.get()

    return financeiro_irko.processa_relatorio_empresas_nexxcera() 


def processa_relatorio_empresas_nexxera_athenas():
    financeiro_athenas = FinanceiroAthenas()
    return financeiro_athenas.processa_relatorio_empresas_nexxcera()


def processsa_dados_operadores():
    # Dados operadores
    api_operadores  = Api(url = "http://diamante2:57773/csp/prgfnc/dash/Operadores")
    dados_operadores = FinanceiroIrko()
    dados_operadores.dados = api_operadores.get()

    # Contagem de operadores por clientes
    api_contagem_master = Api(url = 'http://diamante2:57773/csp/prgfnc/dash/OperadoresMasterPorCliente')
    contagem_operadores = FinanceiroIrko()
    contagem_operadores.dados = api_contagem_master.get()
    
    # Define masters para calcular o grafico de operadores
    contagem_operadores.masters = contagem_operadores.retorna_contagem_operadores()

    return {
        "operadores": dados_operadores.retorna_operadores(),
        "contagem_inteiro": contagem_operadores.retorna_contagem_operadores(),
        "contagem_porcentagem": contagem_operadores.separa_contadores_masters()
    }


def processa_grafico_bancos():
    api_info_bancos = Api(url = "http://diamante2:57773/csp/prgfnc/dash/TotalizadoresBancos")
    dados_bancos = FinanceiroIrko()
    dados_bancos.dados = api_info_bancos.get()
    
    return dados_bancos.retorna_ranking_bancos()