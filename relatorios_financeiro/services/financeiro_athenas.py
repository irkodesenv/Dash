from .financeiro import Financeiro
from conexoes.services.firebird import Conexao


class FinanceiroAthenas(Financeiro):

    def __init__(self):
        super().__init__()  # Chama o construtor da classe pai (Financeiro)
        self.conexao = Conexao()


    def retorna_total_clientes(self, clientes):
        pass
       

    def retorna_qtd_bancos_nexxera_por_cliente(self, clientes):
        pass
        

    def retorna_qtd_clientes_nexxera(self, clientes):
        pass


    def processa_relatorio_empresas_nexxcera(self):
        try:
            data = self.conexao.select("TABFILIAL") \
                                .where("STATUSEMPRESA = 0") \
                                .values("COUNT(*) AS Total, \
                                        COUNT(CASE WHEN HOSTNEXXERA IS NOT NULL AND HOSTNEXXERA <> '' THEN 1 END) AS UsaNexxera, \
                                        COUNT(CASE WHEN HOSTNEXXERA IS NULL OR HOSTNEXXERA = '' THEN 1 END) AS NaoUsaNexxa \
                                        ")\
                                .execute()
            
            obj_retorno = {
                'data':{}
            }

            for row in data:
                total_empresas = row[0]
                empresas_usam_nexxera = row[1]
                empresas_nao_usam_nexxera = row[2]

                if total_empresas > 0:
                    total_em_porcentagem = (empresas_usam_nexxera / total_empresas) *100
                else:
                    total_em_porcentagem = 0
                
                obj_retorno['success'] = True
                obj_retorno['data']['code'] = 200
                obj_retorno['data']['total_clientes'] = total_empresas
                obj_retorno['data']['nexxera'] = {"empresas_nexxera": empresas_usam_nexxera, 
                                                  "empresas_sem_nexxera": empresas_nao_usam_nexxera,
                                                  "porcentagem": f"{total_em_porcentagem:.2f}"}
                return obj_retorno
   
        except Exception as error:
                return self.retorna_obj_error()