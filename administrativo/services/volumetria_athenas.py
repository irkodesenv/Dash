from .Volumetria import Ivolumetria
from conexoes.services.firebird import Conexao

class VolumetriaAthenas(Ivolumetria):   
    
    def __init__(self):
        self.conexao = Conexao()    
    
    def controllerMetricas(self): 
        folha = self.folha() 
        fiscal = self.fiscal()
        financeiro = self.financeiro()
        contabil = self.contabil()
    
        obj_metricas = {
            'folha': self.dict_to_object(folha),
            'fiscal': {},
            'financeiro': {},
            'contabil': {}     
        }
        
        print(obj_metricas)
        
        return obj_metricas
    
    
    def folha(self):
        data = self.conexao.select('TABPESSOAS')\
                            .where("TIPO in ('O', 'N', 'M') AND DATACADASTRO <= '2024-09-30' AND CODIGOEMPRESA = 204")\
                            .values("TIPO, COUNT(CODIGO)")\
                            .group_by("TIPO")\
                            .execute()        
        return data
    
    
    def contratacao(self):
        pass    
    
    
    def fiscal(self):
        pass
    
    
    def financeiro(self):
        pass
    
    
    def contabil(self):
        pass
    
    
    def dict_to_object(self, param):
        return dict(param)
    