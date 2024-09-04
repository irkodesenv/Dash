from conexoes.services.api import Api
from .financeiro_irko import FinanceiroIrko 
from central.settings import URL_API_IRKO


class RelatorioIrkoService:
    def __init__(self, arr_clientes):
        self.arr_clientes = arr_clientes


    def empresas_nexxcera(self):
        parametros = ','.join(map(str, self.arr_clientes))
        api_clientes = Api(url = f"{URL_API_IRKO}/dash/EmpresasFinanceiro/[{parametros}]")
        financeiro_irko = FinanceiroIrko()
        financeiro_irko.dados = api_clientes.get()
 
        if financeiro_irko.dados['success']:
            return financeiro_irko.processa_relatorio_empresas_nexxcera()
        else:
            return financeiro_irko.dados
    

    def dados_operadores(self):
        parametros = ','.join(map(str, self.arr_clientes))
        # Dados operadores
        api_operadores  = Api(url = f"{URL_API_IRKO}/dash/Operadores/[{parametros}]")
        dados_operadores = FinanceiroIrko()
        dados_operadores.dados = api_operadores.get()

        # Contagem de operadores por clientes
        api_contagem_master = Api(url = f"{URL_API_IRKO}/dash/OperadoresMasterPorCliente/[{parametros}]")
        contagem_operadores = FinanceiroIrko()
        contagem_operadores.dados = api_contagem_master.get()
        
        # Define masters para calcular o grafico de operadores
        contagem_operadores.masters = contagem_operadores.retorna_contagem_operadores()

        return {
            "operadores": dados_operadores.retorna_operadores(),
            "contagem_inteiro": contagem_operadores.retorna_contagem_operadores(),
            "contagem_porcentagem": contagem_operadores.separa_contadores_masters()
        }
    

    def bancos(self):
        parametros = ','.join(map(str, self.arr_clientes))
        api_info_bancos = Api(url = f"{URL_API_IRKO}/dash/TotalizadoresBancos/[{parametros}]")
        dados_bancos = FinanceiroIrko()
        dados_bancos.dados = api_info_bancos.get()

        if dados_bancos.dados['success']:
            return dados_bancos.retorna_ranking_bancos()
        else:
            return dados_bancos.dados
        


