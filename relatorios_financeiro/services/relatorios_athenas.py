from .financeiro_athenas import FinanceiroAthenas 
from bancos.services.bancos_financeiros import BancoFinanceiro


class RelatorioAthenasService:
    
    def __init__(self, arr_clientes):
        self.arr_clientes = arr_clientes
        self.banco = BancoFinanceiro()


    def empresas_nexxcera(self):
        financeiro_athenas = FinanceiroAthenas()
        financeiro_athenas.codigo_cliente = self.arr_clientes
        return financeiro_athenas.processa_relatorio_empresas_nexxcera()
    
    
    def ranking_bancos(self):
        self.banco.codigo_cliente = self.arr_clientes
        data = self.banco.retorna_contagem_bancos()

        lista_bancos = [{'Codigo': banco[0], 'QtdeContas': banco[1], 'QtdeClientes': banco[2], 'Nome': banco[0], 'Nome_banco': banco[3]} for banco in data]

        for banco in lista_bancos:
            banco['QtdeContas'] = int(banco['QtdeContas'])

        total_contas = sum(banco['QtdeContas'] for banco in lista_bancos)
        sorted_bancos = sorted(lista_bancos, key=lambda x: x['QtdeContas'], reverse=True)

        # Criar o ranking dos 6 bancos
        ranking_seis_bancos = {}
        for banco in sorted_bancos[:6]:
            nome = banco['Nome']
            quantidade = banco['QtdeContas']
            codigo = banco['Codigo']
            nome_banco = banco['Nome_banco']
            porcentagem = (quantidade / total_contas) * 100
            ranking_seis_bancos[codigo] = {                
                'QtdeContas': quantidade,
                'Porcentagem': round(porcentagem, 2),
                'nome': nome_banco
            }

        # Criar o dicionário de bancos ordenados
        bancos = {banco['Codigo']: {'qtd_contas': banco['QtdeContas'], 'nome': banco['Nome_banco'].upper()[0:14], 'qtd_clientes': banco['QtdeClientes']} for banco in sorted_bancos}
        return {'lista_bancos': bancos, 'ranking_bancos': ranking_seis_bancos}