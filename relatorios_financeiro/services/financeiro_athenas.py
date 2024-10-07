from .financeiro import Financeiro
from conexoes.services.firebird import Conexao
import locale
from datetime import datetime
from decimal import Decimal


class FinanceiroAthenas(Financeiro):

    def __init__(self, datini = None, datfim = None, codigo_cliente = None):
        super().__init__()  # Chama o construtor da classe pai (Financeiro)
        self.conexao = Conexao()
        self.codigo_cliente = None
        self.dat_ini = datini
        self.dat_fim = datfim
        self.codigo_cliente = codigo_cliente
    

    def _where_codigo_empresa(self):
        if self.codigo_cliente:
            return f"tf.CODIGOEMPRESA in ({self.codigo_cliente})"
        return ""


    def retorna_total_clientes(self, clientes):
        return len(clientes)
       

    def retorna_qtd_bancos_nexxera_por_cliente(self, clientes):
        pass
        

    def retorna_qtd_clientes_nexxera(self, clientes):
        if len(clientes)> 0:
            total = 0
            tot_nexxcera = 0
            tot_nao_nexxcera = 0

            for cliente in clientes:
                nexxcera = cliente[1]
                total +=1

                if nexxcera:
                    tot_nexxcera += 1
                else:
                    tot_nao_nexxcera +=1
            
            total_em_porcentagem = (tot_nexxcera / total) *100

            return {
                    "total_empresas": total,
                    "empresas_nexxera": tot_nexxcera, 
                    "empresas_sem_nexxera": tot_nao_nexxcera,
                    "porcentagem": f"{total_em_porcentagem:.2f}"
            }
        else:
            return { 
                "total_empresas": 0,
                "empresas_nexxera": 0, 
                "empresas_sem_nexxera": 0,
                "porcentagem": 0
            }    
            

    def processa_relatorio_empresas_nexxcera(self):
        where = self._where_codigo_empresa()

        try:
            data = self.conexao.select("IRK_SYS_EMPIRK irk") \
                                    .joins("LEFT JOIN TABFILIAL tf ON tf.CODIGOEMPRESA = irk.CODEMP AND tf.CODIGO = 1")\
                                    .values("DISTINCT irk.CODEMP, \
                                            CASE \
                                                WHEN tf.USUARIONEXXERA IS NOT NULL THEN 1\
                                                ELSE\
                                                    0\
                                            END")\
                                    .where(where)\
                                    .execute()
            return {
                'success': True,
                'code': 200,
                'data': {
                    'total_clientes': self.retorna_total_clientes(data),
                    'nexxera': self.retorna_qtd_clientes_nexxera(data)
                }
            }
        except Exception as e:
            self.codigo_retorno = 500
            return self.retorna_obj_error()

    
    #Pagamentos dashirko em tempo real
    def contas_a_pagar_dash(self):
        
        """
            Gera um resumo das informações de pagamentos das empresas com base em um intervalo de datas que estão pendentes.

            Returns:
                dict: Um dicionário contendo os seguintes campos:
                    - data (list of dicts): Lista de dicionários, cada um contendo informações de uma empresa:
                        - codigoempresa (int): Código da empresa.
                        - quantidade_documentos (int): Quantidade de documentos de pagamento.
                        - valor_total (float): Valor total dos pagamentos.
                        - razao (str): Razão social da empresa, limitada a 50 caracteres.
                    - total_quantidade_documentos (int): Quantidade total de documentos de pagamento.
                    - total_valor (str): Valor total dos pagamentos formatado como string monetária.
                    - total_empresas (int): Quantidade total de empresas envolvidas nos pagamentos.

    """
        
        data = self.conexao.select("IRK_SYS_EMPIRK ise") \
                            .joins("INNER JOIN TABLNCFINANCEIRO F ON ise.CODEMP = F.CODIGOEMPRESA \
                                INNER JOIN TABLNCPARCFINANCEIRO P ON (P.IDMASTER = F.IDMASTER)\
                                INNER JOIN TABFILIAL TF ON (TF.CODIGOEMPRESA = ise.CODEMP AND TF.CODIGO = 1)\
                                ")\
                            .values("F.codigoempresa, \
                                    COUNT(P.idmaster) AS quantidade_documentos, \
                                    SUM(P.valor) AS valor_total,\
                                    TF.NOME AS RAZAO,\
                                    COALESCE(SUM(P.REMESSA), 0) AS numero_remessas"
                            )\
                            .where(f"P.DATAVENCIMENTO BETWEEN '{self.dat_ini}' AND '{self.dat_fim}' AND (P.VALORLIQUIDADO = 0 OR P.VALORLIQUIDADO  IS NULL)")\
                            .group_by("F.codigoempresa,TF.NOME")\
                            .order_by("quantidade_documentos DESC")\
                            .execute()
        return data
    
        
    def monta_array_dados(self,data):

        try:
            obj_retorno = {
                'success': True,
                'code': 200,
                'data': {
                    'ListaEmpresas': [],
                    'Totais': {
                        'TotalQuantidadeDocumentos': 0,
                        'TotalValor': 0.0,
                        'TotalEmpresas': 0,
                        'TotalRemessas': 0,
                        'TotalNexxera': 0,
                        'TotalManual': 0
                    }
                }
            }
            
            def formatar_valor(valor):
                valor_str = f"{valor:,.2f}"
                # Substitui as vírgulas (separadores de milhar) por pontos e os pontos (separadores decimais) por vírgulas
                valor_formatado = valor_str.replace(",", "X").replace(".", ",").replace("X", ".")
                return valor_formatado
            
            for item in data:
                empresa_data = {
                    'codigoempresa': item[0],
                    'quantidadedocumentos': item[1],
                    'valortotal': formatar_valor(item[2]),
                    'razao': item[3][:30],
                    'totalremessas': item[4],
                    'doctosfaltantes':item[1] - item[4]

                }
                
                obj_retorno['data']['ListaEmpresas'].append(empresa_data)
                obj_retorno['data']['Totais']['TotalQuantidadeDocumentos'] += item[1]
                obj_retorno['data']['Totais']['TotalValor'] += item[2]
                obj_retorno['data']['Totais']['TotalEmpresas'] += 1
                obj_retorno['data']['Totais']['TotalRemessas'] += item[4]
                obj_retorno['data']['Totais']['TotalNexxera'] =0
                #obj_retorno['data']['Totais']['TotalManual'] =0

            total_manual= obj_retorno['data']['Totais']['TotalQuantidadeDocumentos'] - obj_retorno['data']['Totais']['TotalRemessas'] - obj_retorno['data']['Totais']['TotalNexxera']
            
            obj_retorno['data']['Totais']['TotalManual'] = total_manual
            #obj_retorno['data']['Totais']['TotalValor'] = locale.format_string('%.2f', obj_retorno['data']['Totais']['TotalValor'], grouping=True)

            return obj_retorno

        except Exception as e:
            print(e)
            self.codigo_retorno = 500
            return self.retorna_obj_error()
        

#Pagamentos dashirko em tempo real
    def doctos_indefinidos(self):
        
        """
            Gera um resumo das informações de documentos indefinidos das empresas com base em um intervalo de datas que estão pendentes.

            Returns:
                dict: Um dicionário contendo os seguintes campos:
                    - data (list of dicts): Lista de dicionários, cada um contendo informações de uma empresa:
                        - codcli (int): Código da empresa.
                        - Nome : Nome da empresa.
                        - valor_total (float): Valor total dos pagamentos.
                        - razao (str): Razão social da empresa, limitada a 50 caracteres.
                    

    """
        
        data = self.conexao.select("IRK_SYS_EMPIRK ise") \
                            .joins("INNER JOIN TABLNCFINANCEIRO F ON ise.CODEMP = F.CODIGOEMPRESA \
                                INNER JOIN TABLNCPARCFINANCEIRO P ON (P.IDMASTER = F.IDMASTER)\
                                INNER JOIN TABFILIAL TF ON (TF.CODIGOEMPRESA = ise.CODEMP AND TF.CODIGO = 1)\
                                INNER JOIN TABPESSOAS TP ON (TP.CODIGO = F.CODIGOPESSOA)")\
                            .values("F.codigoempresa, \
                                    TF.NOME, \
                                    P.valor,\
                                    COALESCE(f.NUMERODOCUMENTOFISCAL, p.NUMERODOCUMENTO) AS NUMERODOCUMENTO,\
                                    TP.NOME AS Fornecedor,\
                                    COALESCE (p.REMESSA,0) AS remessa,\
                                    p.DATAVENCIMENTO"
                            )\
                            .where(f"P.DATAVENCIMENTO BETWEEN '{self.dat_ini}' AND '{self.dat_fim}' AND (P.VALORLIQUIDADO = 0 OR P.VALORLIQUIDADO  IS NULL) AND (p.REMESSA = 0 OR p.REMESSA IS NULL)")\
                            .execute()
        return data


    def monta_array_dados_doctos_indefinidos(self,data):


        try:
            obj_retorno = {
                'success': True,
                'code': 200,
                'data': {
                    'ListaIndefinidos': [],
                }
            }
            
            def formatar_valor(valor):
                valor_str = f"{valor:,.2f}"
                valor_formatado = valor_str.replace(",", "X").replace(".", ",").replace("X", ".")
                return valor_formatado

            # Processando cada item da lista de tuplas
            for item in data:
                codigo, empresa, valor, documento, fornecedor,remessa,data_vencimento = item
                valor_formatado = formatar_valor(valor)
                if documento is None:
                    documento=""
                
                #formatar data
                data_vencimento_formatada = data_vencimento.strftime("%d/%m/%Y")

                documento = {
                    "CodCli": str(codigo),
                    "DescricaoEmpresa": empresa,
                    "DataEmissao": "08/08/2024", 
                    "CodigoFornecedor": "6", 
                    "DescricaoFornecedor": fornecedor,
                    "CNPJCPF": "0",
                    "TipoDocumento": "",
                    "NumeroDocumento": documento, 
                    "Valor": valor_formatado,
                    "Parcela": "1", 
                    "DataVencimento": data_vencimento_formatada, 
                    "DataPagamento": "",
                    "ValorLiquido": str(int(valor * 100)),
                    "ValorPago": "0",
                    "Historico": "",
                    "Banco": "",
                    "Agencia": "",
                    "Conta": "",
                    "BancoRemessa": "",
                    "NumeroRemessa": "",
                    "FlagFof": "2",
                    "FlagNexxera": "0",
                    "Status": "0",
                    'Color': "#384551" if remessa == 1 else "#ff3e1d"
                }
                
                obj_retorno['data']['ListaIndefinidos'].append(documento)
            
            return obj_retorno

        except Exception as e:
            print(e)
            return {
                'success': False,
                'code': 500,
                'message': str(e)
            }
        

    #Ranking de doctos indefinidos
    def ranking_doctos_indefinidos(self):
        
        """
            Gera um resumo das informações de pagamentos das empresas com base em um intervalo de datas que estão pendentes.

            Returns:
                dict: Um dicionário contendo os seguintes campos:
                    - data (list of dicts): Lista de dicionários, cada um contendo informações de uma empresa:
                        - codigoempresa (int): Código da empresa.
                        - quantidade_documentos (int): Quantidade de documentos de pagamento.
                        - valor_total (float): Valor total dos pagamentos.
                        - razao (str): Razão social da empresa, limitada a 50 caracteres.
                    - total_quantidade_documentos (int): Quantidade total de documentos de pagamento.
                    - total_valor (str): Valor total dos pagamentos formatado como string monetária.
                    - total_empresas (int): Quantidade total de empresas envolvidas nos pagamentos.

    """
        
        data = self.conexao.select("IRK_SYS_EMPIRK ise") \
                            .joins("INNER JOIN TABLNCFINANCEIRO F ON ise.CODEMP = F.CODIGOEMPRESA \
                                INNER JOIN TABLNCPARCFINANCEIRO P ON (P.IDMASTER = F.IDMASTER)\
                                INNER JOIN TABFILIAL TF ON (TF.CODIGOEMPRESA = ise.CODEMP AND TF.CODIGO = 1)\
                                ")\
                            .values("F.codigoempresa, \
                                    COUNT(P.idmaster) AS quantidade_documentos, \
                                    SUM(P.valor) AS valor_total,\
                                    TF.NOME AS RAZAO,\
                                    COALESCE(SUM(P.REMESSA), 0) AS numero_remessas"
                            )\
                            .where(f"P.DATAVENCIMENTO BETWEEN '{self.dat_ini}' AND '{self.dat_fim}' AND (P.VALORLIQUIDADO = 0 OR P.VALORLIQUIDADO  IS NULL) AND (p.REMESSA = 0 OR p.REMESSA IS NULL)")\
                            .group_by("F.codigoempresa,TF.NOME")\
                            .order_by("quantidade_documentos DESC")\
                            .execute()
        return data
    

    def doctos_gerais(self,codigo_empresa):
        """
            Gera um resumo das informações de documentos indefinidos das empresas com base em um intervalo de datas que estão pendentes.

            Returns:
                dict: Um dicionário contendo os seguintes campos:
                    - data (list of dicts): Lista de dicionários, cada um contendo informações de uma empresa:
                        - codcli (int): Código da empresa.
                        - Nome : Nome da empresa.
                        - valor_total (float): Valor total dos pagamentos.
                        - razao (str): Razão social da empresa, limitada a 50 caracteres.
                    

    """
        
        data = self.conexao.select("IRK_SYS_EMPIRK ise") \
                            .joins("INNER JOIN TABLNCFINANCEIRO F ON ise.CODEMP = F.CODIGOEMPRESA \
                                INNER JOIN TABLNCPARCFINANCEIRO P ON (P.IDMASTER = F.IDMASTER)\
                                INNER JOIN TABFILIAL TF ON (TF.CODIGOEMPRESA = ise.CODEMP AND TF.CODIGO = 1)\
                                INNER JOIN TABPESSOAS TP ON (TP.CODIGO = F.CODIGOPESSOA)")\
                            .values("F.codigoempresa, \
                                    TF.NOME, \
                                    P.valor,\
                                    COALESCE(f.NUMERODOCUMENTOFISCAL, p.NUMERODOCUMENTO) AS NUMERODOCUMENTO,\
                                    TP.NOME AS Fornecedor,\
                                    COALESCE (p.REMESSA,0) AS remessa,\
                                    p.DATAVENCIMENTO"
                            )\
                            .where(f"P.DATAVENCIMENTO BETWEEN '{self.dat_ini}' AND '{self.dat_fim}' AND ise.CODEMP='{codigo_empresa}' AND (P.VALORLIQUIDADO = 0 OR P.VALORLIQUIDADO  IS NULL)")\
                            .order_by("remessa ASC,P.valor DESC")\
                            .execute()
        return data
    

    def monta_array_dados_doctos_gerais(self,data):


        try:
            obj_retorno = {
                'success': True,
                'code': 200,
                'data': {
                    'ListaCliente': [],
                }
            }
            
            def formatar_valor(valor):
                valor_str = f"{valor:,.2f}"
                valor_formatado = valor_str.replace(",", "X").replace(".", ",").replace("X", ".")
                return valor_formatado

            # Processando cada item da lista de tuplas
            for item in data:
                codigo, empresa, valor, documento, fornecedor,remessa,data_vencimento = item
                valor_formatado = formatar_valor(valor)
                if documento is None:
                    documento=""
                
                #formatar data
                data_vencimento_formatada = data_vencimento.strftime("%d/%m/%Y")

                documento = {
                    "CodCli": str(codigo),
                    "DescricaoEmpresa": empresa,
                    "DataEmissao": "08/08/2024", 
                    "CodigoFornecedor": "6", 
                    "DescricaoFornecedor": fornecedor,
                    "CNPJCPF": "0",
                    "TipoDocumento": "",
                    "NumeroDocumento": documento, 
                    "Valor": valor_formatado,
                    "Parcela": "1", 
                    "DataVencimento": data_vencimento_formatada, 
                    "DataPagamento": "",
                    "ValorLiquido": str(int(valor * 100)),
                    "ValorPago": "0",
                    "Historico": "",
                    "Banco": "",
                    "Agencia": "",
                    "Conta": "",
                    "BancoRemessa": "",
                    "NumeroRemessa": "",
                    "FlagFof": "2",
                    "FlagNexxera": "0",
                    "Status": "0",
                    'Color': "#384551" if remessa == 1 else "#ff3e1d"
                }
                
                obj_retorno['data']['ListaCliente'].append(documento)
            
            return obj_retorno

        except Exception as e:
            print(e)
            return {
                'success': False,
                'code': 500,
                'message': str(e)
            }
            
                   
    def retorna_conta_correntes(self, data_fim, codigo_empresa):
        where_clause = f"TIPOCONTA = 1 AND DTREG <= '{data_fim}'"

        if codigo_empresa:
            where_clause += f" AND CODIGOEMPRESA in ({codigo_empresa})"    
            
        data = self.conexao.select("TABCONTABANCARIA") \
                            .values("CODIGOEMPRESA, CODIGO, NOME, AGENCIA, CONTA, CODIGOBANCO, CONTACONTABIL")\
                            .where(where_clause)\
                            .execute()      
        return data
    
    
    def retorna_qtd_transacoes(self, tipo, data_ini, data_fim, codigo_empresa):        
        where_clause = f"DATAREGISTRO BETWEEN '{data_ini}' AND '{data_fim}' AND TIPO in {tipo}"

        if codigo_empresa:
            where_clause += f" AND CODIGOEMPRESA in ({codigo_empresa})" 

        data = self.conexao.select("TABLNCFINANCEIRO lf") \
                            .joins("INNER JOIN TABLNCPARCFINANCEIRO pf ON lf.IDMASTER = pf.IDMASTER ")\
                            .where(where_clause) \
                            .values("CASE WHEN TIPO = 'P' THEN 'Pagamentos' WHEN TIPO = 'R' THEN 'Recebimentos' ELSE 'Não definido' END, COUNT(TIPO)") \
                            .group_by("lf.TIPO")\
                            .execute()
        return data

    
    def retorna_variacao_cambial(self, data_ini, data_fim, codigo_empresa):
        where_clause = f"VC.DATA BETWEEN '{data_ini}' AND '{data_fim}'"

        if codigo_empresa:
            where_clause += f" AND CODIGOEMPRESA in ({codigo_empresa})"
            
        data = self.conexao.select("TABLNCFINANCEIRO F") \
                        .joins("INNER JOIN TABVARIACAOCAMBIAL VC ON (F.IDMASTER = VC.IDMASTERFINANCEIRO)")\
                        .where(where_clause) \
                        .values("COUNT(F.IDMASTER)") \
                        .execute()               
        return data[0][0]