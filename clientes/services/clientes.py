from abc import abstractmethod


class Cliente:

    def __init__(self):
        self.codigo_cliente = None
        self.razao_social = None
        self.cpf_cnpj = None


    @abstractmethod
    def retorna_cadastro(self):
        pass
