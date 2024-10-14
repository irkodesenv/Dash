from .Volumetria import Ivolumetria
from conexoes.services.firebird import Conexao
from .volumetria_folha import Folha
from .volumetria_financeiro import Financeiro
from .volumetria_contabil import Contabil
from .volumetria_fiscal import Fiscal
from accounts.services.pessoa import Pessoa
from accounts.services.funcionario import Funcionario
from relatorios_financeiro.services.financeiro_athenas import FinanceiroAthenas
from contabil.services.contabil_athenas import ContabilAthenas
from fiscal.services.fiscal_service import FiscalAthenas
from utils.views import media_periodo_range_data

class VolumetriaAthenas(Ivolumetria):   
    
    def __init__(self, conexao, data_ini = None, data_fim = None, codigo_empresa = None, data_comparativo_ini = None, data_comparativo_fim = None, filial = None):
        self.conexao = conexao  
        self.codigo_empresa = codigo_empresa
        self.filial = filial
        self.data_ini = data_ini
        self.data_fim = data_fim
        self.data_comparativo_ini = data_comparativo_ini
        self.data_comparativo_fim = data_comparativo_fim
        
        
    def controllerFolha(self, demonstracao):
        media_realizado = demonstracao
        media_comparativo = demonstracao
        
        if demonstracao == 2:
            media_realizado = media_periodo_range_data([self.data_ini, self.data_fim])
            media_comparativo = media_periodo_range_data([self.data_comparativo_ini, self.data_comparativo_fim])
        
        funcionario = Funcionario(self.conexao)
        
        # Realizado
        competencia_atual = Folha(funcionario, codigo_empresa = self.codigo_empresa, data_ini = self.data_ini, data_fim = self.data_fim, codigo_filial = self.filial)  
        periodo_realizado = competencia_atual.controller_folha(media_realizado)
            
        # Comparativo
        competencia_anterior = Folha(funcionario, codigo_empresa = self.codigo_empresa, data_ini = self.data_comparativo_ini, data_fim = self.data_comparativo_fim, codigo_filial = self.filial)
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
        financeiro_atual = Financeiro(financeiro_athenas, codigo_empresa = self.codigo_empresa, data_ini = self.data_ini, data_fim = self.data_fim, codigo_filial = self.filial)
        periodo_realizado = financeiro_atual.controller_financeiro_volumetria(media_realizado)
        
        # Comparativo
        financeiro_anterior = Financeiro(financeiro_athenas, codigo_empresa = self.codigo_empresa, data_ini = self.data_comparativo_ini, data_fim = self.data_comparativo_fim, codigo_filial = self.filial)
        metricas = financeiro_anterior.controller_financeiro_volumetria_comparativo(periodo_realizado, media_comparativo)
        
        return metricas    
            
    
    def controllerFiscal(self, demonstracao):
        media_realizado = demonstracao
        media_comparativo = demonstracao
        
        if demonstracao == 2:
            media_realizado = media_periodo_range_data([self.data_ini, self.data_fim])
            media_comparativo = media_periodo_range_data([self.data_comparativo_ini, self.data_comparativo_fim])
        
        fiscal_athenas = FiscalAthenas(self.conexao)
        
        # Realizado
        contabil_atual = Fiscal(fiscal_athenas, codigo_empresa = self.codigo_empresa, data_ini = self.data_ini, data_fim = self.data_fim, codigo_filial = self.filial)
        periodo_realizado = contabil_atual.controller_fiscal_volumetria(media_realizado)
        
        # Comparativo
        competencia_anterior = Fiscal(fiscal_athenas, codigo_empresa = self.codigo_empresa, data_ini = self.data_comparativo_ini, data_fim = self.data_comparativo_fim, codigo_filial = self.filial)
        metricas = competencia_anterior.controller_fiscal_volumetria_comparativo(periodo_realizado, media_comparativo)
        
        return metricas
    

    def controllerContabil(self, demonstracao):
        media_realizado = demonstracao
        media_comparativo = demonstracao
        
        if demonstracao == 2:
            media_realizado = media_periodo_range_data([self.data_ini, self.data_fim])
            media_comparativo = media_periodo_range_data([self.data_comparativo_ini, self.data_comparativo_fim])
            
        contabil_athenas = ContabilAthenas(self.conexao)
        
        # Realizado
        contabil_atual = Contabil(contabil_athenas, codigo_empresa = self.codigo_empresa, data_ini = self.data_ini, data_fim = self.data_fim, codigo_filial = self.filial)
        periodo_realizado = contabil_atual.controller_contabil_volumetria(media_realizado)
        
        # Comparativo
        competencia_anterior = Contabil(contabil_athenas, codigo_empresa = self.codigo_empresa, data_ini = self.data_comparativo_ini, data_fim = self.data_comparativo_fim, codigo_filial = self.filial)
        metricas = competencia_anterior.controller_contabil_volumetria_comparativo(periodo_realizado, media_comparativo)
            
        return metricas