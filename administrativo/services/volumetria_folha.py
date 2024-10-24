

class Folha:
    
    def __init__(self, pessoa, codigo_empresa = None, data_ini = None, data_fim = None, codigo_filial = None):
        self.pessoa = pessoa 
        self.data_ini = data_ini
        self.data_fim = data_fim
        self.codigo_empresa = codigo_empresa    
        self.codigo_filial = codigo_filial
    
    def controller_folha(self, media):
        folha = {
            "Autônomos": 0,
            "Funcionários CLT": 0,
            "Pró Labore":0,
            "Estagiários": 0,
            "Admissões": 0,
            "Demissões": 0          
        }      
        
        if not media:
            media = 1
        
        contagem_tipo_funcionarios_realizado = self.pessoa.conta_tipo_funcionario(('O', 'N', 'M'), self.data_fim, self.codigo_empresa, self.codigo_filial)

        for tipo, quantidade in contagem_tipo_funcionarios_realizado.items():
            qtd_dividido_por_media = int(quantidade / media)
            folha[tipo] = {
                "orcado": 0,
                "realizado": qtd_dividido_por_media,
                "realizado_x_orcado": qtd_dividido_por_media - 0,
                "percent": (qtd_dividido_por_media * 0) / 100                
            }            
        
        # Estagiarios
        qtd_estagiarios = self.pessoa.contar_estagiarios(self.data_fim, self.codigo_empresa, self.codigo_filial)    
        qtd_estagiario_dividido_por_media = int(qtd_estagiarios / media)    
        folha["Estagiários"] = {
                "orcado": 0,
                "realizado": qtd_estagiario_dividido_por_media,
                "realizado_x_orcado": qtd_estagiario_dividido_por_media - 0,
                "percent": (qtd_estagiario_dividido_por_media * 0 ) / 100      
            }
        
        # Admissoes
        qtd_admissoes = self.pessoa.contar_admissoes(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_adm_dividido_por_media = int(qtd_admissoes / media)  
        folha["Admissões"] = {
                "orcado": 0,
                "realizado": qtd_adm_dividido_por_media,
                "realizado_x_orcado": qtd_adm_dividido_por_media - 0,
                "percent": (qtd_adm_dividido_por_media * 0) / 100        
            }
        
        # Demissoes
        qtd_demissoes = self.pessoa.contar_demissoes(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_demi_dividido_por_media = int(qtd_demissoes / media)  
        folha["Demissões"] = {
                "orcado": 0,
                "realizado": qtd_demi_dividido_por_media,
                "realizado_x_orcado": qtd_demi_dividido_por_media - 0,
                "percent": (qtd_demi_dividido_por_media * 0) / 100    
            }
                 
        return folha
    
    
    def controller_folha_comparativo(self, folha, media):
        if not media:
            media = 1  
                  
        contagem_tipo_funcionarios_realizado = self.pessoa.conta_tipo_funcionario(('O', 'N', 'M'), self.data_fim, self.codigo_empresa, self.codigo_filial)
    
        for item, quantidade in contagem_tipo_funcionarios_realizado.items():
            qtd_dividido_por_media = int(quantidade / media)            
            folha[item].update({
                "comparativo": qtd_dividido_por_media,
                "realizado_x_comparativo": folha[item]['realizado'] - qtd_dividido_por_media,
                "percent_rc": f"{round(((folha[item]['realizado'] - qtd_dividido_por_media) / qtd_dividido_por_media) * 100 ,2)}" if qtd_dividido_por_media != 0 else 0  
            })
            
        # Estagiarios
        qtd_estagiarios = self.pessoa.contar_estagiarios(self.data_fim, self.codigo_empresa, self.codigo_filial) 
        qtd_estagiario_dividido_por_media = int(qtd_estagiarios / media)   
        folha["Estagiários"].update({               
                "comparativo": qtd_estagiario_dividido_por_media,
                "realizado_x_comparativo": folha['Estagiários']['realizado'] - qtd_estagiario_dividido_por_media,
                "percent_rc": f"{round(((folha['Estagiários']['realizado'] - qtd_estagiario_dividido_por_media) / qtd_estagiario_dividido_por_media) * 100, 2)}" if qtd_estagiario_dividido_por_media != 0 else 0  
            })
        
        # Admissoes
        qtd_admissoes = self.pessoa.contar_admissoes(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_adm_dividido_por_media = int(qtd_admissoes / media)  
        folha["Admissões"].update({
                "comparativo": qtd_adm_dividido_por_media,
                "realizado_x_comparativo": folha['Admissões']['realizado'] - qtd_adm_dividido_por_media,
                "percent_rc": f"{round(((folha['Admissões']['realizado'] - qtd_adm_dividido_por_media) / qtd_adm_dividido_por_media) * 100 ,2)}" if qtd_adm_dividido_por_media != 0 else 0        
            })
        
        # Demissoes
        qtd_demissoes = self.pessoa.contar_demissoes(self.data_ini, self.data_fim, self.codigo_empresa, self.codigo_filial)
        qtd_demi_dividido_por_media = int(qtd_demissoes / media)
        
        folha["Demissões"].update({
                "comparativo": qtd_demi_dividido_por_media,
                "realizado_x_comparativo": folha['Demissões']['realizado'] - qtd_demi_dividido_por_media,           
                "percent_rc": f"{round(((folha['Demissões']['realizado'] - qtd_demi_dividido_por_media) / qtd_demi_dividido_por_media) * 100, 2)}" if qtd_demi_dividido_por_media != 0 else 0         
            })
        
        

        return folha