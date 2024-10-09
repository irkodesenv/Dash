class Fiscal:
    
    def __init__(self, fiscal, codigo_empresa = None, data_ini = None, data_fim = None):
        self.fiscal = fiscal
        self.data_ini = data_ini
        self.data_fim = data_fim
        self.codigo_empresa = codigo_empresa 
        
        
    def controller_fiscal_volumetria(self, media):
        fiscal = {}
        
        if not media:
            media = 1
            
        # Entrada / Saida
        qtd_transacoes = self.fiscal.retorna_qtd_entrada_saida_produto(self.data_ini, self.data_fim, self.codigo_empresa)
        for tipo, quantidade in qtd_transacoes:
            qtd_dividido_por_media = int(quantidade / media)
            fiscal[tipo.strip()] = {
                "orcado": 0,
                "realizado": qtd_dividido_por_media,
                "realizado_x_orcado": qtd_dividido_por_media - 0,
                "percent": (qtd_dividido_por_media * 0) / 100                
            }
            
        
        # Qtd importacoes        
        qtd_importacoes = self.fiscal.retorna_qtd_importacoes(self.data_ini, self.data_fim, self.codigo_empresa)
        qtd_media_dividido_importacoes = int(qtd_importacoes / media)

        fiscal["Importações"] = {
            "orcado": 0,
            "realizado": qtd_media_dividido_importacoes,
            "realizado_x_orcado": qtd_media_dividido_importacoes - 0,
            "percent": (qtd_media_dividido_importacoes * 0) / 100                
        } 
        
        
        # Filiais
        qtd_filiais = self.fiscal.retorna_qtd_filiais(self.data_fim, self.codigo_empresa)
        qtd_media_dividido_filiais = int(qtd_filiais / media)

        fiscal["Filiais"] = {
            "orcado": 0,
            "realizado": qtd_media_dividido_filiais,
            "realizado_x_orcado": qtd_media_dividido_filiais - 0,
            "percent": (qtd_media_dividido_filiais * 0) / 100                
        } 
        
        
        # SKU movimentado
        sku_movimentado = 0
        qtd_media_dividido_importacoes = int(sku_movimentado / media)

        fiscal["SKU Movimentado"] = {
            "orcado": 0,
            "realizado": 0,
            "realizado_x_orcado": 0 - 0,
            "percent": (0 * 0) / 100                
        } 
        
        
        # Estoque (Entrada)
        sku_movimentado = 0
        qtd_media_dividido_importacoes = int(sku_movimentado / media)

        fiscal["Estoque (Entrada)"] = {
            "orcado": 0,
            "realizado": 0,
            "realizado_x_orcado": 0 - 0,
            "percent": (0 * 0) / 100                
        } 
        
        
        # Estoque (Saida)
        sku_movimentado = 0
        qtd_media_dividido_importacoes = int(sku_movimentado / media)

        fiscal["Estoque (Saída)"] = {
            "orcado": 0,
            "realizado": 0,
            "realizado_x_orcado": 0 - 0,
            "percent": (0 * 0) / 100                
        } 
           
        return fiscal
    
    
    def controller_fiscal_volumetria_comparativo(self, fiscal, media):
        if not media:
            media = 1
        
        # Entrada / Saida
        qtd_transacoes = self.fiscal.retorna_qtd_entrada_saida_produto(self.data_ini, self.data_fim, self.codigo_empresa)
        for tipo, quantidade in qtd_transacoes:
            qtd_dividido_por_media = int(quantidade / media)   
            # Medida paliativa para tratar quando ha movimento em um mes e não tiver no outro  
            try:       
                fiscal[tipo.strip()].update({
                    "comparativo": qtd_dividido_por_media,
                    "realizado_x_comparativo": fiscal[tipo.strip()]['realizado'] - qtd_dividido_por_media,
                    "percent_rc": round(((fiscal[tipo.strip()]['realizado'] - qtd_dividido_por_media) / qtd_dividido_por_media) * 100 ,2) if quantidade != 0 else 0  
                })
            except Exception as e:
                fiscal[tipo.strip()] = {
                    "orcado": 0,
                    "realizado": 0,
                    "realizado_x_orcado": 0,
                    "percent": 0,            
                    "comparativo": qtd_dividido_por_media,
                    "realizado_x_comparativo": 0 - qtd_dividido_por_media,
                    "percent_rc": round(((0 - qtd_dividido_por_media) / qtd_dividido_por_media) * 100 ,2) if quantidade != 0 else 0  
                }
          
                
        # Qtd importacoes        
        qtd_importacoes = self.fiscal.retorna_qtd_importacoes(self.data_ini, self.data_fim, self.codigo_empresa)
        qtd_media_dividido_importacoes = int(qtd_importacoes / media)
        
        fiscal["Importações"].update({
            "comparativo": qtd_media_dividido_importacoes,
            "realizado_x_comparativo": fiscal['Importações']['realizado'] - qtd_media_dividido_importacoes,
            "percent_rc": round(((fiscal['Importações']['realizado'] - qtd_media_dividido_importacoes) / qtd_media_dividido_importacoes),2) * 100 if qtd_media_dividido_importacoes != 0 else 0             
        })  
        
        
        # Filiais
        qtd_filiais = self.fiscal.retorna_qtd_filiais(self.data_fim, self.codigo_empresa)
        qtd_media_dividido_filiais = int(qtd_filiais / media)
        
        fiscal["Filiais"].update({
            "comparativo": qtd_media_dividido_filiais,
            "realizado_x_comparativo": fiscal['Filiais']['realizado'] - qtd_media_dividido_filiais,
            "percent_rc": round(((fiscal['Filiais']['realizado'] - qtd_media_dividido_filiais) / qtd_media_dividido_filiais),2) * 100 if qtd_media_dividido_filiais != 0 else 0             
        }) 
        
        
        # SKU movimentado
        sku_movimentado = 0
        qtd_media_dividido_sku = int(sku_movimentado / media)
        
        fiscal["SKU Movimentado"].update({
            "comparativo": qtd_media_dividido_sku,
            "realizado_x_comparativo": fiscal['SKU Movimentado']['realizado'] - qtd_media_dividido_sku,
            "percent_rc": round(((fiscal['SKU Movimentado']['realizado'] - qtd_media_dividido_sku) / qtd_media_dividido_sku),2) * 100 if qtd_media_dividido_sku != 0 else 0             
        }) 
        
        
        # Estoque (Entrada)
        sku_estoque_entrada = 0
        qtd_media_dividido_estoque_entrada = int(sku_estoque_entrada / media)
        
        fiscal["Estoque (Entrada)"].update({
            "comparativo": qtd_media_dividido_estoque_entrada,
            "realizado_x_comparativo": fiscal['Estoque (Entrada)']['realizado'] - qtd_media_dividido_estoque_entrada,
            "percent_rc": round(((fiscal['Estoque (Entrada)']['realizado'] - qtd_media_dividido_estoque_entrada) / qtd_media_dividido_estoque_entrada),2) * 100 if qtd_media_dividido_estoque_entrada != 0 else 0             
        }) 
        
        # Estoque (Saida)
        sku_estoque_saida = 0
        qtd_media_dividido_estoque_saida = int(sku_estoque_saida / media)
        
        fiscal["Estoque (Saída)"].update({
            "comparativo": qtd_media_dividido_estoque_saida,
            "realizado_x_comparativo": fiscal['Estoque (Saída)']['realizado'] - qtd_media_dividido_estoque_saida,
            "percent_rc": round(((fiscal['Estoque (Saída)']['realizado'] - qtd_media_dividido_estoque_saida) / qtd_media_dividido_estoque_saida),2) * 100 if qtd_media_dividido_estoque_saida != 0 else 0             
        }) 
        
        return fiscal