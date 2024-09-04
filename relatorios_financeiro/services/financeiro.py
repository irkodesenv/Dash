from abc import abstractmethod

class Financeiro:

    def __init__(self):
        self.codigo_retorno = 200
        self.obj_retorno = { 'data':{} }

        
    def retorna_obj_error(self):

        self.obj_retorno['success'] = False
        self.obj_retorno['data']['code'] = 500
        self.obj_retorno['data']['message'] = "Não foi possível retornar dados."
        
        return self.obj_retorno
    
    
    @abstractmethod
    def retorna_total_clientes(self, clientes):
        pass


    @abstractmethod
    def retorna_qtd_clientes_nexxera(self, clientes):
        pass


    @abstractmethod
    def processa_relatorio_empresas_nexxcera(self):
        pass


    @abstractmethod
    def retorna_ranking_bancos(self):
        pass


    def calcular_porcentagens(self, dados):
        # Calcula o total das quantidades
        total = sum(dados.values())
        
        # Calcula as porcentagens
        porcentagens = {}
        for chave, valor in dados.items():
            porcentagem = (valor / total) * 100
            porcentagens[chave] = round(porcentagem, 2)  # Arredonda para 2 casas decimais
        
        return porcentagens
    

    def separa_contadores_masters(self):

        master = {            
            'nao_master': None,
            'master': None,
            'dos_masters': {}
        }

        for indice, value in self.masters.items():

            if indice == "master":
                master['master'] = value

            if indice == "nao_master":
                master['nao_master'] = value

            if indice == "mais_de_um_master":
                master['dos_masters']['mais_de_um_master'] = value

            if indice == "apenas_um_master":
                master['dos_masters']['apenas_um_master'] = value

        # Calcula porcentagem de masters e nao master
        total_masters_x_nao_masteres = self.calcular_porcentagens(  {'nao_master': master['nao_master'], 'master': master['master']}  )

        # Calcula mais de 1 masters e apenas 1
        total_mais_de_um_x_apenas_um = self.calcular_porcentagens(  {'mais_de_um_master': master['dos_masters']['mais_de_um_master'], 'apenas_um_master': master['dos_masters']['apenas_um_master']}  )

        return {**total_masters_x_nao_masteres, **total_mais_de_um_x_apenas_um}