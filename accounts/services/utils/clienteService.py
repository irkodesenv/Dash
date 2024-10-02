from ..cliente import Cliente
from typing import List, Dict, Any, Tuple

class ClienteService:
    
    def __init__(self, conexao):
        self.conexao = conexao
        self.cliente = Cliente(self.conexao)
    
    
    def obter_clientes(self) -> List[Tuple[Any, Any, Any]]:
        return self.cliente.lista_cadastros()
    
    
    def obter_descendentes(self, codigo_cliente):    
        descendentes = self.cliente.lista_cadastro_descendentes(codigo_cliente)   
        return self.formata_dados_clientes_formulario(descendentes)

    
    def formata_dados_clientes_formulario(self, clientes) -> List[Dict[str, Any]]:
        cliente_dados = [
            {
                'Codigo': cliente[0],
                'CNPJ': cliente[2],
                'Razao': cliente[1]
            }
            for cliente in clientes if cliente[0] and cliente[1] and cliente[2]
        ]
        return cliente_dados
    

    def obter_clientes_formatados_formulario(self) -> List[Dict[str, Any]]:
        clientes = self.obter_clientes()
        return self.formata_dados_clientes_formulario(clientes)
