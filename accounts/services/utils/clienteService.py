from ..cliente import Cliente

class ClienteService:
    
    def __init__(self, conexao):
        self.conexao = conexao
        self.cliente = Cliente(self.conexao)
    
    
    def obter_clientes(self):
        return self.cliente.lista_cadastros()

    
    def formata_dados_clientes_formulario(self, clientes):
        cliente_dados = [
            {
                'Codigo': cliente[0],
                'CNPJ': cliente[2],
                'Razao': cliente[1]
            }
            for cliente in clientes if cliente[0] and cliente[1] and cliente[2]
        ]
        return cliente_dados
    

    def obter_clientes_formatados_formulario(self):
        clientes = self.obter_clientes()
        return self.formata_dados_clientes_formulario(clientes)
