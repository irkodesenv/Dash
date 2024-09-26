from .Volumetria import Ivolumetria
from conexoes.services.firebird import Conexao
from .volumetria_folha import Folha
from .volumetria_financeiro import Financeiro 
from accounts.services.pessoa import Pessoa

class VolumetriaAthenas(Ivolumetria):   
    
    def __init__(self, conexao, data_ini = None, data_fim = None, codigo_empresa = None):
        self.conexao = conexao  
        self.codigo_empresa = codigo_empresa
        self.data_ini = data_ini
        self.data_fim = data_fim
        
        
    def controllerMetricas(self): 
    
        # Folha
        metricas_folha = self.controllerFolha()
            

        obj_metricas = {
            'folha': metricas_folha,
            'fiscal': {},
            'financeiro': {},
            'contabil': {}     
        }
        
        return obj_metricas
    
    
    def controllerFolha(self):        
        pessoa = Pessoa(self.conexao)
        competencia_atual = Folha(pessoa, codigo_empresa = self.codigo_empresa, data_ini = self.data_ini, data_fim = self.data_fim)  

        periodo_realizado = competencia_atual.controller_folha()
        
        data_ini_comparativo = '2024-08-01'
        data_fim_comparativo = '2024-08-30' 
        
        competencia_anterior = Folha(pessoa, codigo_empresa = self.codigo_empresa, data_ini = data_ini_comparativo, data_fim = data_fim_comparativo)
        
        metricas = competencia_anterior.controller_folha_comparativo(periodo_realizado)
        
        return metricas