from .clientes import Cliente


class ClienteIrko(Cliente):

    def __init__(self):
        self.codigo_empresa = None
        self.razao_social = None
        self.cpf_cnpj = None
        self.arr_dados = None


    def retorna_cadastro(self):
        pass