class Contabil:
    
    def __init__(self, contabil, codigo_empresa = None, data_ini = None, data_fim = None, codigo_filial = None):
        self.contabil = contabil
        self.data_ini = data_ini
        self.data_fim = data_fim
        self.codigo_empresa = codigo_empresa
        self.codigo_filial = codigo_filial
        
        
    def controller_contabil_volumetria(self, media):
        contabil = {}
        
        if not media:
            media = 1
            
        # Lancto contabeis    
        qtd_lcts_contabeis = self.contabil.retorna_qtd_lctos_contabeis(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_dividido_por_media_lcts_contabeis = int(qtd_lcts_contabeis / media)   
        
        contabil["Lançtos Contábeis"] = {
            "orcado": 0,
            "realizado": qtd_dividido_por_media_lcts_contabeis,
            "realizado_x_orcado": qtd_dividido_por_media_lcts_contabeis - 0,
            "percent": (qtd_dividido_por_media_lcts_contabeis * 0) / 100                
        }   
        
        
        # Partidas contabeis
        qtd_partidas_contabeis = self.contabil.retorna_qtd_partidas_contabeis(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_dividido_por_media_partida_contabeis = int(qtd_partidas_contabeis / media)   
        
        contabil["Partidas Contábeis"] = {
            "orcado": 0,
            "realizado": qtd_dividido_por_media_partida_contabeis,
            "realizado_x_orcado": qtd_dividido_por_media_partida_contabeis - 0,
            "percent": (qtd_dividido_por_media_partida_contabeis * 0) / 100                
        } 
        
        
        # Ativo imobilizado
        qtd_ativos_imobilizados = self.contabil.retorna_qtd_ativo_imobilizado(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_dividido_por_media_ativo_imobilizado = int(qtd_ativos_imobilizados / media)   
        
        contabil["Ativo Imobilizado"] = {
            "orcado": 0,
            "realizado": qtd_dividido_por_media_ativo_imobilizado,
            "realizado_x_orcado": qtd_dividido_por_media_ativo_imobilizado - 0,
            "percent": (qtd_dividido_por_media_ativo_imobilizado * 0) / 100                
        } 
        
        return contabil
    
    
    def controller_contabil_volumetria_comparativo(self, contabil, media):
        if not media:
            media = 1
        
        # Lancto contabeis    
        qtd_lcts_contabeis = self.contabil.retorna_qtd_lctos_contabeis(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_dividido_por_media_lcts_contabeis = int(qtd_lcts_contabeis / media)   
        
        contabil["Lançtos Contábeis"].update({
            "comparativo": qtd_dividido_por_media_lcts_contabeis,
            "realizado_x_comparativo": contabil['Lançtos Contábeis']['realizado'] - qtd_dividido_por_media_lcts_contabeis,
            "percent_rc": round(((contabil['Lançtos Contábeis']['realizado'] - qtd_dividido_por_media_lcts_contabeis) / qtd_dividido_por_media_lcts_contabeis),2) * 100 if qtd_dividido_por_media_lcts_contabeis != 0 else 0       
        })
        
        
        # Partidas contabeis
        qtd_partidas_contabeis = self.contabil.retorna_qtd_partidas_contabeis(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_dividido_por_media_partida_contabeis = int(qtd_partidas_contabeis / media)  
        
        contabil["Partidas Contábeis"].update({
            "comparativo": qtd_dividido_por_media_partida_contabeis,
            "realizado_x_comparativo": contabil['Partidas Contábeis']['realizado'] - qtd_dividido_por_media_partida_contabeis,
            "percent_rc": round(((contabil['Partidas Contábeis']['realizado'] - qtd_dividido_por_media_partida_contabeis) / qtd_dividido_por_media_partida_contabeis),2) * 100 if qtd_dividido_por_media_partida_contabeis != 0 else 0       
        })
        
        
        # Ativo imobilizado
        qtd_ativos_imobilizados = self.contabil.retorna_qtd_ativo_imobilizado(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_dividido_por_media_ativo_imobilizado = int(qtd_ativos_imobilizados / media) 
        
        contabil["Ativo Imobilizado"].update({
            "comparativo": qtd_dividido_por_media_ativo_imobilizado,
            "realizado_x_comparativo": contabil['Ativo Imobilizado']['realizado'] - qtd_dividido_por_media_ativo_imobilizado,
            "percent_rc": round(((contabil['Ativo Imobilizado']['realizado'] - qtd_dividido_por_media_ativo_imobilizado) / qtd_dividido_por_media_ativo_imobilizado),2) * 100 if qtd_dividido_por_media_ativo_imobilizado != 0 else 0       
        })
        
        return contabil