
from .clientes_irko import ClienteIrko
from conexoes.services.api import Api
from central.settings import URL_API_IRKO


class ControllerClienteIrko:

    def __init__(self, arr_clientes):
        self.class_cliente_irko = ClienteIrko() 
        self.codigo_cliente = arr_clientes
        self.dados = None


    def retorna_cadastro_clientes(self):
        api_clientes = Api(url = f"{URL_API_IRKO}/dash/empresasIrko/{self.codigo_cliente}")
        cadastros_clientes = ClienteIrko()
        cadastros_clientes.arr_dados = api_clientes.get()

        if cadastros_clientes.arr_dados['success']:
            return cadastros_clientes.arr_dados
        else:
            return cadastros_clientes.arr_dados
        

    def retorna_contas_a_pagar_dash(self):
        #trocar Api
        api_clientes = Api(url = f"{URL_API_IRKO}/dash/AgendamentosPendentes")

        pagamentos_pendentes = ClienteIrko()
        pagamentos_pendentes.arr_dados = api_clientes.get()

        if pagamentos_pendentes.arr_dados['success']:
            return pagamentos_pendentes.arr_dados
        else:
            return pagamentos_pendentes.arr_dados
        

    def retorna_doctos_irko_indefinidos(self):
        #trocar Api
        api_doctos = Api(url = f"{URL_API_IRKO}/dash/ListaDocIndefinidos")
        
        doctos_indefinidos = ClienteIrko()
        doctos_indefinidos.arr_dados = api_doctos.get()

        if doctos_indefinidos.arr_dados['success']:
            return doctos_indefinidos.arr_dados
        else:
            return doctos_indefinidos.arr_dados