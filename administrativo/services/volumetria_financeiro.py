
class Financeiro:
    
    def __init__(self, financeiro, codigo_empresa = None, data_ini = None, data_fim = None, codigo_filial = None):
        self.financeiro = financeiro
        self.data_ini = data_ini
        self.data_fim = data_fim
        self.codigo_empresa = codigo_empresa    
        self.codigo_filial = codigo_filial  
        
  
    def controller_financeiro_volumetria(self, media):    
        financeiro = {
            "Contas Correntes": 0,
            "Pagamentos": 0,
            "Recebimentos":0,
            "Fechamento Câmbio": 0,
            "Reembolso Despesa": 0       
        } 
        
        if not media:
            media = 1
        
        # Contas correntes      
        contas_correntes = self.financeiro.retorna_conta_correntes(self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_dividido_por_media_contas = int(len(contas_correntes) / media)
        
        financeiro["Contas Correntes"] = {
            "orcado": 0,
            "realizado": len(contas_correntes),
            "realizado_x_orcado": qtd_dividido_por_media_contas - 0,
            "percent": (qtd_dividido_por_media_contas * 0) / 100                
        }   
        
        # Transacoes
        transacoes = self.financeiro.retorna_qtd_transacoes(('R', 'P'), self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)        
        for tipo, quantidade in transacoes:
            qtd_dividido_por_media = int(quantidade / media)
            financeiro[tipo.strip()] = {
                "orcado": 0,
                "realizado": qtd_dividido_por_media,
                "realizado_x_orcado": qtd_dividido_por_media - 0,
                "percent": (qtd_dividido_por_media * 0) / 100                
            }
            
        # Variacao cambial 
        variacao_cambial = self.financeiro.retorna_variacao_cambial(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_dividido_por_variacao_cambial = int(variacao_cambial / media)
        
        financeiro["Fechamento Câmbio"] = {
            "orcado": 0,
            "realizado": qtd_dividido_por_variacao_cambial,
            "realizado_x_orcado": qtd_dividido_por_variacao_cambial - 0,
            "percent": (qtd_dividido_por_variacao_cambial * 0) / 100                
        }          
        
        # Reembolso Despesa
        reembolso_despesa = self.financeiro.retorna_qtd_relatorio_despesa(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_dividido_por_RD = int(reembolso_despesa / media)
        
        financeiro["Reembolso Despesa"] = {
            "orcado": 0,
            "realizado": reembolso_despesa,
            "realizado_x_orcado": qtd_dividido_por_RD - 0,
            "percent": (qtd_dividido_por_RD * 0) / 100                
        }    
        
        return financeiro
    
    
    def controller_financeiro_volumetria_comparativo(self, financeiro, media):
         
        if not media:
            media = 1
        
        # Contas correntes      
        contas_correntes = self.financeiro.retorna_conta_correntes(self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_dividido_por_media_contas = int(len(contas_correntes) / media)
        
        financeiro["Contas Correntes"].update({
            "comparativo": qtd_dividido_por_media_contas,
            "realizado_x_comparativo": financeiro['Contas Correntes']['realizado'] - qtd_dividido_por_media_contas,      
            "percent_rc": f"{round(((financeiro['Contas Correntes']['realizado'] - qtd_dividido_por_media_contas) / qtd_dividido_por_media_contas),2)}" if qtd_dividido_por_media_contas != 0 else 0   
        })
        
        
        # Transacoes
        transacoes = self.financeiro.retorna_qtd_transacoes(('R', 'P'), self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)        
        for tipo, quantidade in transacoes:
            qtd_dividido_por_media = int(quantidade / media)   
            # Medida paliativa para tratar quando ha movimento em um mes e não tiver no outro  
            try:       
                financeiro[tipo.strip()].update({
                    "comparativo": qtd_dividido_por_media,
                    "realizado_x_comparativo": financeiro[tipo.strip()]['realizado'] - qtd_dividido_por_media,  
                    "percent_rc": f"{round(((financeiro[tipo.strip()]['realizado'] - qtd_dividido_por_media) / qtd_dividido_por_media) * 100 ,2)}" if qtd_dividido_por_media != 0 else 0                    
                })
            except Exception as e:
                financeiro[tipo.strip()] = {
                    "orcado": 0,
                    "realizado": 0,
                    "realizado_x_orcado": 0,
                    "percent": 0,            
                    "comparativo": qtd_dividido_por_media,
                    "realizado_x_comparativo": 0 - qtd_dividido_por_media,
                    "percent_rc": round(((0 - qtd_dividido_por_media) / qtd_dividido_por_media) * 100 ,2) if quantidade != 0 else 0  
                }
            
            
        # Variacao cambial 
        variacao_cambial = self.financeiro.retorna_variacao_cambial(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_dividido_por_variacao_cambial = int(variacao_cambial / media)
        
        financeiro["Fechamento Câmbio"].update({
            "comparativo": qtd_dividido_por_variacao_cambial,
            "realizado_x_comparativo": financeiro['Fechamento Câmbio']['realizado'] - qtd_dividido_por_variacao_cambial,           
            "percent_rc": f"{round(((financeiro['Fechamento Câmbio']['realizado'] - qtd_dividido_por_variacao_cambial) / qtd_dividido_por_variacao_cambial) * 100, 2)}" if qtd_dividido_por_variacao_cambial != 0 else 0                  
        }) 
        

        # Reembolso Despesa
        reembolso_despesa = self.financeiro.retorna_qtd_relatorio_despesa(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_dividido_por_RD = int(reembolso_despesa / media)
        
        financeiro["Reembolso Despesa"].update({
            "comparativo": qtd_dividido_por_RD,
            "realizado_x_comparativo": financeiro['Reembolso Despesa']['realizado'] - qtd_dividido_por_RD,
            "percent_rc": f"{round(((financeiro['Reembolso Despesa']['realizado'] - qtd_dividido_por_RD) / qtd_dividido_por_RD) * 100, 2)}" if qtd_dividido_por_RD != 0 else 0                  
        })        

        return financeiro  