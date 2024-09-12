
from .clientes_athenas import ClienteAthenas


class ControllerClienteAthenas:

    def __init__(self, arr_clientes):
        self.cliente_athenas = ClienteAthenas() 
        self.codigo_cliente = arr_clientes
        self.dados = None


    def retorna_cadastro_clientes(self):
        self.cliente_athenas.codigo_empresa = self.codigo_cliente
        return self._processa_clientes()


    def _processa_clientes(self):
        try:
            clientes = self.cliente_athenas.retorna_cadastro()
            return self._formata_dados_clientes(clientes)
        except Exception as e:
            raise RuntimeError("Erro ao processar clientes: " + str(e))


    def _formata_dados_clientes(self, clientes):
        cliente_dados = [
            {
                'Codigo': cliente[0],
                'CNPJ': cliente[2],
                'Razao': cliente[1]
            }
            for cliente in clientes if cliente[0] and cliente[1] and cliente[2]
        ]
        return cliente_dados
