from .financeiro import Financeiro
from collections import defaultdict
from pprint import pprint
import json

class FinanceiroIrko(Financeiro):


    def retorna_total_clientes(self, clientes):
        """
            Retorna o total de clientes a partir dos dados fornecidos.

            Args:
                clientes (dict): Um dicionário contendo os dados dos clientes.
            
            Exemplos de uso: 
                financeiro_irko = FinanceiroIrko(url = "XXXXXX")
                financeiro_irko.processa_api()
                dados_clientes = {
                    'data': {
                        'ListaEmpresas': [
                            {'nome': 'Empresa A', 'id': 1},
                            {'nome': 'Empresa B', 'id': 2},
                            # Mais empresas...
                        ]
                    }
                }      
                financeiro_irko.retorna_total_clientes(result)

            Returns:
                int: O número total de clientes, ou 0 se os dados estiverem ausentes ou incompletos.
        """

        if 'data' in clientes and 'ListaEmpresas' in clientes['data']:
            return len(clientes['data']['ListaEmpresas'])
        else:
            return 0


    def retorna_qtd_bancos_nexxera_por_cliente(self, clientes):
        """
            Retorna a quantidade de bancos nexxera e não nexxera a partir dos dados fornecidos.

            Args:
                clientes (dict): Um dicionário contendo os dados das empresas e seus bancos.

            Exemplos de uso: 
                financeiro_irko = FinanceiroIrko(url = "XXXXXX")   
                financeiro_irko.processa_api()             
                dados_clientes = {
                    'data': {
                        'ListaEmpresas': [
                            {
                                'NomeEmpresa': 'Empresa A',
                                'Bancos': [
                                    {'NomeBanco': 'Banco X', 'Flgnexxera': '1'},
                                    {'NomeBanco': 'Banco Y', 'Flgnexxera': '0'},
                                    # Mais bancos...
                                ]
                            },
                            # Mais empresas...
                        ]
                    }
                }   
                financeiro_irko.retorna_total_clientes(result)
            
            Returns:
                dict: Um dicionário contendo a contagem total de bancos, bancos nexxera e bancos não nexxera.
                    Retorna 0 para cada contagem se os dados estiverem ausentes ou incompletos.
        """

        if 'data' in clientes and 'ListaEmpresas' in clientes['data']:
            bancos_nexxera = 0
            bancos_sem_nexxecera = 0
            total = 0

            for empresa in clientes['data']['ListaEmpresas']:
                for bancos in empresa['Bancos']:
                    total += len(bancos)

                    for banco in bancos:
                        if banco['Flgnexxera'] == "1":
                            bancos_nexxera += 1
                        else:
                            bancos_sem_nexxecera += 1

            return {
                "total_bancos": total, 
                "bancos_nexxera": bancos_nexxera, 
                "bancos_sem_nexxera": bancos_sem_nexxecera
            }
        else:
            return {
                "total_bancos": 0, 
                "bancos_nexxera": 0, 
                "bancos_sem_nexxera": 0
            }
        

    def retorna_qtd_clientes_nexxera(self, clientes):
        """
            Retorna a quantidade de Clientes que usam Nexxera

            Args:
                clientes (dict): Um dicionário contendo os dados das empresas e seus bancos.

            Exemplos de uso: 
                financeiro_irko = FinanceiroIrko(url = "XXXXXX")   
                financeiro_irko.processa_api()             
                dados_clientes = {
                    'data': {
                        'ListaEmpresas': [
                            {
                                'NomeEmpresa': 'Empresa A',
                                'nexxera': [0 -> Sem nexxera ou 1 -> Com nexxera]
                            },
                            # Mais empresas...
                        ]
                    }
                }   
                financeiro_irko.retorna_total_clientes(result)
            
            Returns:
                dict: Um dicionário contendo a contagem total de Clientes, Clientes Nexxera e Clientes não Nexxera.
        """

        if 'data' in clientes and 'ListaEmpresas' in clientes['data']:
            empresas_nexxera = 0
            empresas_sem_nexxecera = 0
            total = 0

            for empresa in clientes['data']['ListaEmpresas']:
                total += 1
                if empresa['Nexxera'] == "1":
                    empresas_nexxera += 1
                else:
                    empresas_sem_nexxecera += 1
            
            total_em_porcentagem = 0

            if empresas_nexxera:
                total_em_porcentagem = (empresas_nexxera / total) *100

            return {
                "total_empresas": total,
                "empresas_nexxera": empresas_nexxera, 
                "empresas_sem_nexxera": empresas_sem_nexxecera,
                "porcentagem": f"{total_em_porcentagem:.2f}"
            }
        else:
            return { 
                "total_empresas": 0,
                "empresas_nexxera": 0, 
                "empresas_sem_nexxcera": 0,
                "porcentagem": 0
            }
        

    def processa_relatorio_empresas_nexxcera(self):

        obj_retorno = {
            'data':{}
        }

        try:
            if 'success' in self.dados:
                obj_retorno['success'] = True
                obj_retorno['data']['code'] = self.dados['code']
                obj_retorno['data']['total_clientes'] = self.retorna_total_clientes(self.dados)
                obj_retorno['data']['nexxera'] = self.retorna_qtd_clientes_nexxera(self.dados)
            else:
                self.codigo_retorno = self.dados['code']
                return self.retorna_obj_error()
            
            return obj_retorno
        except Exception as error:
                self.codigo_retorno = 500
                return self.retorna_obj_error()


    def retorna_contagem_operadores(self):

        total_nao_master = 0
        total_master = 0
        total_mais_de_um_master = 0
        total_um_master = 0

        if 'success' in self.dados:
            for indice, values in self.dados.items():
                if indice == "data":
                    for empresa in values['ListaEmpresa']:
                        # Possui master
                        if int(empresa['QtdeMaster']) > 0:
                            total_master += int(empresa['QtdeMaster'])
                            # Mais de um Master
                            if int(empresa['QtdeMaster']) > 1:
                                total_mais_de_um_master += 1
                            else:
                                total_um_master += 1
                        else:
                            total_master += 0
                            total_mais_de_um_master += 0
                            total_um_master += 0                           
                    
                        total_nao_master += int(empresa['QtdeNaoMaster'])

            return {
                "master": total_master,
                "nao_master": total_nao_master,
                "mais_de_um_master": total_mais_de_um_master,
                "apenas_um_master": total_um_master
            }
        else:
            return {
                "master": 0,
                "nao_master": 0,
                "mais_de_um_master": 0,
                "apenas_um_master": 0
            }      


    def retorna_operadores(self):
        lista_usuario = []

        if 'success' in self.dados:
            for indice, values in self.dados.items():
                if indice == "data":                    
                    for usuario in values['ListaOperadores']:

                        id_usuario = usuario['Usuario']
                        nome_completo = usuario['Nome']
                        arr_nome = nome_completo.split()
                        
                        iniciais = arr_nome[0][0:1] + arr_nome[1][0:1]

                        operador = usuario['DadosOperador']

                        lista_usuario.append({'id_usuario': id_usuario, "nome": nome_completo[0:24], "iniciais": iniciais, "bancos": operador})
            return lista_usuario  
        else:
            lista_usuario.append({'id_usuario': '', "nome": '', "iniciais": '', "bancos": ''})
            return lista_usuario   
        

    def retorna_ranking_bancos(self):

        lista_bancos = self.dados['data']['ListaBancos']

        # Converter a quantidade de contas para inteiros
        for banco in lista_bancos:
            banco['QtdeContas'] = int(banco['QtdeContas'])

        total_contas = sum(banco['QtdeContas'] for banco in lista_bancos)

        # Ordenar os bancos pela quantidade de contas (do maior para o menor)
        sorted_bancos = sorted(lista_bancos, key=lambda x: x['QtdeContas'], reverse=True)

        # Criar o ranking dos 6 bancos
        ranking_seis_bancos = {}
        for banco in sorted_bancos[:6]:
            nome = banco['Nome']
            quantidade = banco['QtdeContas']
            codigo = banco['Codigo']
            porcentagem = (quantidade / total_contas) * 100
            ranking_seis_bancos[codigo] = {                
                'QtdeContas': quantidade,
                'Porcentagem': round(porcentagem, 2),
                'nome': nome
            }

        # Criar o dicionário de bancos ordenados
        bancos = {banco['Codigo']: {'qtd_contas': banco['QtdeContas'], 'nome': banco['Nome'][0:14], 'qtd_clientes': banco['QtdeClientes']} for banco in sorted_bancos}
        
        return {'lista_bancos': bancos, 'ranking_bancos': ranking_seis_bancos}
