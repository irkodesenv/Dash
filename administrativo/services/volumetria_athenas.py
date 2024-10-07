from .Volumetria import Ivolumetria
from conexoes.services.firebird import Conexao
from .volumetria_folha import Folha
from .volumetria_financeiro import Financeiro 
from accounts.services.pessoa import Pessoa
from accounts.services.funcionario import Funcionario
from relatorios_financeiro.services.financeiro_athenas import FinanceiroAthenas
from utils.views import media_periodo_range_data

class VolumetriaAthenas(Ivolumetria):   
    
    def __init__(self, conexao, data_ini = None, data_fim = None, codigo_empresa = None, data_comparativo_ini = None, data_comparativo_fim = None):
        self.conexao = conexao  
        self.codigo_empresa = codigo_empresa
        self.data_ini = data_ini
        self.data_fim = data_fim
        self.data_comparativo_ini = data_comparativo_ini
        self.data_comparativo_fim = data_comparativo_fim
        
        
    def controllerMetricas(self, demonstracao): 
        media_realizado = demonstracao
        media_comparativo = demonstracao
        
        if demonstracao == 2:
            media_realizado = media_periodo_range_data([self.data_ini, self.data_fim])
            media_comparativo = media_periodo_range_data([self.data_comparativo_ini, self.data_comparativo_fim])
            
        # Folha
        #metricas_folha = self.viewFolha(media_realizado, media_comparativo)
        metricas_folha = ""
        
        # Financeiro
        #metricas_financeiro = self.ViewFinanceiro(media_realizado, media_comparativo)
        metricas_financeiro = ""
        # Fiscal
        metricas_fiscal = self.controllerFiscal(media_realizado, media_comparativo)
        
        # Contabil
        metricas_contabil = self.controllerContabil(media_realizado, media_comparativo)
        
        obj_metricas = {
            'folha': metricas_folha,
            'financeiro': metricas_financeiro,
            'fiscal': metricas_fiscal,            
            'contabil': metricas_contabil     
        }
        
        return obj_metricas
    
    
    def controllerFolha(self, demonstracao):
        media_realizado = demonstracao
        media_comparativo = demonstracao
        
        if demonstracao == 2:
            media_realizado = media_periodo_range_data([self.data_ini, self.data_fim])
            media_comparativo = media_periodo_range_data([self.data_comparativo_ini, self.data_comparativo_fim])
        
        funcionario = Funcionario(self.conexao)
        
        # Realizado
        competencia_atual = Folha(funcionario, codigo_empresa = self.codigo_empresa, data_ini = self.data_ini, data_fim = self.data_fim)  
        periodo_realizado = competencia_atual.controller_folha(media_realizado)
            
        # Comparativo
        competencia_anterior = Folha(funcionario, codigo_empresa = self.codigo_empresa, data_ini = self.data_comparativo_ini, data_fim = self.data_comparativo_fim)
        metricas = competencia_anterior.controller_folha_comparativo(periodo_realizado, media_comparativo)
        
        return metricas
            
    
    def controllerFinanceiro(self, demonstracao):
        media_realizado = demonstracao
        media_comparativo = demonstracao
        
        if demonstracao == 2:
            media_realizado = media_periodo_range_data([self.data_ini, self.data_fim])
            media_comparativo = media_periodo_range_data([self.data_comparativo_ini, self.data_comparativo_fim])
            
        financeiro_athenas = FinanceiroAthenas()  
        
        # Realizado
        financeiro_atual = Financeiro(financeiro_athenas, codigo_empresa = self.codigo_empresa, data_ini = self.data_ini, data_fim = self.data_fim)
        periodo_realizado = financeiro_atual.controller_financeiro_volumetria(media_realizado)
        
        # Comparativo
        financeiro_anterior = Financeiro(financeiro_athenas, codigo_empresa = self.codigo_empresa, data_ini = self.data_comparativo_ini, data_fim = self.data_comparativo_fim)
        metricas = financeiro_anterior.controller_financeiro_volumetria_comparativo(periodo_realizado, media_comparativo)
        
        return metricas    
            
    
    def controllerFiscal(self, media_realizado, media_comparativo):
        return {"teste": ""}
    

    def controllerContabil(self, media_realizado, media_comparativo):
        return {"teste": ""}