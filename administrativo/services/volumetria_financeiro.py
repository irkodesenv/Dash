
from conexoes.services.firebird import Conexao

class Financeiro:
    
    def __init__(self, codigo_empresa = None, data_ini = None, data_fim = None):
        self.conexao = Conexao()
        self.data_cadastro = None
        self.codigo_empresa = None    
        
  
    def retorna_contas_a_pagar(self):
        pass