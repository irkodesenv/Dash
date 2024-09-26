

class Folha:
    
    def __init__(self, pessoa, codigo_empresa = None, data_ini = None, data_fim = None):
        self.pessoa = pessoa 
        self.data_ini = data_ini
        self.data_fim = data_fim
        self.codigo_empresa = codigo_empresa    
        
    
    def controller_folha(self):
        folha = {}
        
        contagem_tipo_funcionarios_realizado = self.pessoa.conta_tipo_funcionario(('O', 'N', 'M'), self.data_fim, self.codigo_empresa)

        for tipo, quantidade in contagem_tipo_funcionarios_realizado.items():
            folha[tipo] = {
                "orcado": 0,
                "realizado": quantidade,
                "realizado_x_orcado": quantidade - 0,
                "percent": (quantidade * 0) / 100                
            }            
        
        # Estagiarios
        qtd_estagiarios = self.pessoa.contar_estagiarios(self.data_fim, self.codigo_empresa)        
        folha["Estagiários"] = {
                "orcado": 0,
                "realizado": qtd_estagiarios,
                "realizado_x_orcado": qtd_estagiarios - 0,
                "percent": (qtd_estagiarios * 0 ) / 100      
            }
        
        # Admissoes
        qtd_admissoes = self.pessoa.contar_admissoes(self.data_ini, self.data_fim, self.codigo_empresa)
        folha["Admissões"] = {
                "orcado": 0,
                "realizado": qtd_admissoes,
                "realizado_x_orcado": qtd_admissoes - 0,
                "percent": (qtd_admissoes * 0) / 100        
            }
        
        # Demissoes
        qtd_demissoes = self.pessoa.contar_demissoes(self.data_ini, self.data_fim, self.codigo_empresa)
        folha["Demissões"] = {
                "orcado": 0,
                "realizado": qtd_demissoes,
                "realizado_x_orcado": qtd_demissoes - 0,
                "percent": (qtd_demissoes * 0) / 100    
            }
                 
        return folha
    
    
    def controller_folha_comparativo(self, folha):        
        contagem_tipo_funcionarios_realizado = self.pessoa.conta_tipo_funcionario(('O', 'N', 'M'), self.data_fim, self.codigo_empresa)
    
        for item, quantidade in contagem_tipo_funcionarios_realizado.items():            
            folha[item].update({
                "comparativo": quantidade,
                "realizado_x_comparativo": folha[item]['realizado'] - quantidade,
                "percent_rc": round(((folha[item]['realizado'] - quantidade) / quantidade) * 100 ,2) if quantidade != 0 else 0  
            })
            
        # Estagiarios
        qtd_estagiarios = self.pessoa.contar_estagiarios(self.data_fim, self.codigo_empresa) 
        folha["Estagiários"].update({               
                "comparativo": qtd_estagiarios,
                "realizado_x_comparativo": folha['Estagiários']['realizado'] - qtd_estagiarios,
                "percent_rc": round(((folha['Estagiários']['realizado'] - qtd_estagiarios) / qtd_estagiarios),2) * 100 if qtd_estagiarios != 0 else 0        
            })
        
        # Admissoes
        qtd_admissoes = self.pessoa.contar_admissoes(self.data_ini, self.data_fim, self.codigo_empresa)
        folha["Admissões"].update({
                "comparativo": qtd_admissoes,
                "realizado_x_comparativo": folha['Admissões']['realizado'] - qtd_admissoes,
                "percent_rc": round(((folha['Admissões']['realizado'] - qtd_admissoes) / qtd_admissoes) * 100 ,2) if qtd_admissoes != 0 else 0      
            })
        
        # Demissoes
        qtd_demissoes = self.pessoa.contar_demissoes(self.data_ini, self.data_fim, self.codigo_empresa)
        folha["Demissões"].update({
                "comparativo": qtd_demissoes,
                "realizado_x_comparativo": folha['Demissões']['realizado'] - qtd_demissoes,
                "percent_rc": round(((folha['Demissões']['realizado'] - qtd_demissoes) / qtd_demissoes) * 100,2) if qtd_demissoes != 0 else 0      
            })

        return folha