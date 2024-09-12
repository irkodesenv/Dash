from relatorios_financeiro.services.financeiro_athenas import FinanceiroAthenas
from relatorios_financeiro.services.relatorios_irko import RelatorioIrkoService
from clientes.services.clientes_irko import ClienteIrko
from conexoes.services.api import Api
from central.settings import URL_API_IRKO


from clientes.services.controller_irko import ControllerClienteIrko
from datetime import datetime
from typing import Optional


class DashboardService:
    def __init__(self, array_clientes: Optional[int] = None, datini: Optional[int] = None, datfim: Optional[int] = None):
        self.array_clientes = array_clientes
        self.dat_ini = datini
        self.dat_fim = datfim

    def recupera_pagamentos_athenas(self):
        
        self.dat_ini = datetime.strptime(self.dat_ini, '%d/%m/%Y')
        datini = self.dat_ini.strftime('%m/%d/%Y')

        self.dat_fim = datetime.strptime(self.dat_fim, '%d/%m/%Y')
        datfim = self.dat_fim.strftime('%m/%d/%Y')
        dados_athenas = FinanceiroAthenas(datini, datfim)
        dados_dash_athenas = dados_athenas.contas_a_pagar_dash()

        # Tratar dados e transformar em array
        array_dados_dash = dados_athenas.monta_array_dados(dados_dash_athenas)

        return array_dados_dash
    

    def recupera_pagamentos_irko(self):

        dados_irko = ControllerClienteIrko(None)

        return dados_irko.retorna_contas_a_pagar_dash(self.dat_ini,self.dat_fim)
    

    def combina_dados_athenas_irko(self,dados_athenas,dados_irko):

        # Verifica se ambas as respostas foram bem-sucedidas
        if not (dados_athenas['success'] and dados_athenas['success']):
            return {'success': False, 'code': 500, 'data': {'message': 'Erro ao processar os dados.'}}

        
        lista_empresas_irko = dados_irko.get('data', {}).get('ListaEmpresas', [])
        lista_empresas_athenas = dados_athenas.get('data', {}).get('ListaEmpresas', [])

        lista_empresas_combinada = lista_empresas_irko + lista_empresas_athenas

        totais_athenas = dados_athenas.get('data', {}).get('Totais', [])
        
        totais_irko = dados_irko.get('data', {}).get('Totais', [])
        
        def to_float(value):
            return float(value.replace('.', '').replace(',', '.'))

        def to_int(value):
            return int(value)
        
        def safe_float(value):
            try:
                return float(value.replace('.', '').replace(',', '.'))
            except (ValueError, AttributeError):
                return 0.0
            
        totais_somados = {
            'TotalQuantidadeDocumentos': to_int(totais_athenas.get('TotalQuantidadeDocumentos', 0)) + to_int(totais_irko.get('TotalQuantidadeDocumentos', 0)),
            'TotalValor': (totais_athenas.get('TotalValor', '0')) + to_float(totais_irko.get('TotalValor', '0')),
            'TotalEmpresas': to_int(totais_athenas.get('TotalEmpresas', 0)) + to_int(totais_irko.get('TotalEmpresas', 0)),
            'TotalRemessas': to_int(totais_athenas.get('TotalRemessas', 0)) + to_int(totais_irko.get('TotalRemessas', 0)),
            'TotalNexxera': to_int(totais_athenas.get('TotalNexxera', 0)) + to_int(totais_irko.get('TotalNexxera', 0)),
            'TotalManual': to_int(totais_athenas.get('TotalManual', 0)) + to_int(totais_irko.get('TotalManual', 0))
        }
        
        lista_empresas_combinada.sort(key=lambda empresa: safe_float(empresa.get('valortotal', '0')), reverse=True)
        #lista_empresas_combinada.sort(key=lambda empresa: int(empresa.get('quantidadedocumentos', empresa.get('quantidade_documentos', '0'))), reverse=True)

        obj_retorno_combinado = {
                'success': True,
                'code': 200,
                'data': {
                    'ListaEmpresas': lista_empresas_combinada,
                    'Totais': totais_somados
                }
            }
        return obj_retorno_combinado


    def recupera_doctos_indenifidos_irko(self):

        dados_irko = ControllerClienteIrko(None)

        return dados_irko.retorna_doctos_irko_indefinidos(self.dat_ini,self.dat_fim)
    

    def recupera_doctos_indefinidos_athenas(self):

        self.dat_ini = datetime.strptime(self.dat_ini, '%d/%m/%Y')
        datini = self.dat_ini.strftime('%m/%d/%Y')

        self.dat_fim = datetime.strptime(self.dat_fim, '%d/%m/%Y')
        datfim = self.dat_fim.strftime('%m/%d/%Y')
        dados_athenas = FinanceiroAthenas(datini, datfim)
        dados_indefinidos_athenas = dados_athenas.doctos_indefinidos()

        pass
        #tratar dados e transformar em array
        array_dados_indefinidos =  dados_athenas.monta_array_dados_doctos_indefinidos(dados_indefinidos_athenas)

        return array_dados_indefinidos
    

    def combina_dados_doctos_athenas_irko(self,dados_athenas,dados_irko):


        # Verifica se ambas as respostas foram bem-sucedidas
        if not (dados_athenas['success'] and dados_athenas['success']):
            return {'success': False, 'code': 500, 'data': {'message': 'Erro ao processar os dados.'}}

        
        lista_doctos_irko = dados_irko.get('data', {}).get('ListaIndefinidos', [])
        lista_doctos_athenas = dados_athenas.get('data', {}).get('ListaIndefinidos', [])

        lista_doctos_combinada = lista_doctos_irko + lista_doctos_athenas
        
        def parse_data_vencimento(data_str):
            try:
                return datetime.strptime(data_str, '%d/%m/%Y')
            except ValueError:
                return datetime.min 
            
        lista_doctos_combinada.sort(
            key=lambda empresa: (
                int(empresa.get('CodCli', '0')), 
                parse_data_vencimento(empresa.get('DataVencimento', '31/12/9999'))  # Ordena por data de vencimento
            ),
            reverse=False
        )

        #lista_doctos_combinada.sort(key=lambda empresa: int(empresa.get('CodCli', '0')), reverse=False)

        obj_retorno_combinado = {
                'success': True,
                'code': 200,
                'data': {
                    'ListaIndefinidos': lista_doctos_combinada
                }
            }
        return obj_retorno_combinado
    

    def recupera_ranking_doctos_indefinidos_athenas(self):

        #hoje filtramos apenas pelo dia atual
        hoje = datetime.now()
        datini = hoje.strftime('%m/%d/%Y')
        datfim = datini

        #datini="08/01/2024"
        dados_athenas = FinanceiroAthenas(datini,datfim)
        # passar datini = dtahoje
        dados_ranking_athenas = dados_athenas.ranking_doctos_indefinidos()

        #tratar dados e transformar em array
        array_dados_ranking =  dados_athenas.monta_array_dados(dados_ranking_athenas)
        print(array_dados_ranking)

        return array_dados_ranking
    

    def recupera_doctos_gerais_athenas(self,codigo_empresa):

        self.dat_ini = datetime.strptime(self.dat_ini, '%d/%m/%Y')
        datini = self.dat_ini.strftime('%m/%d/%Y')

        self.dat_fim = datetime.strptime(self.dat_fim, '%d/%m/%Y')
        datfim = self.dat_fim.strftime('%m/%d/%Y')

        dados_athenas = FinanceiroAthenas(datini, datfim)

        dados_gerais_athenas = dados_athenas.doctos_gerais(codigo_empresa)
        pass
        #tratar dados e transformar em array
        array_dados_gerais =  dados_athenas.monta_array_dados_doctos_gerais(dados_gerais_athenas)
        
        return array_dados_gerais
    

    def recupera_dctos_gerais_irko(self):
        array_dados=[
            self.dat_ini.replace('/','-'),
            self.dat_fim.replace('/','-'),
            self.array_clientes
        ]
 
        #trocar Api
        api_doctos = Api(url = f"{URL_API_IRKO}/dash/ListaDocPorCliente/{array_dados}")
 
        doctos_gerais = ClienteIrko()
        doctos_gerais.arr_dados = api_doctos.get()

        if doctos_gerais.arr_dados['success']:
            return doctos_gerais.arr_dados
        else:
            return doctos_gerais.arr_dados