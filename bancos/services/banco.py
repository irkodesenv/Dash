from abc import ABC, abstractmethod

class IBanco(ABC):

    def __init__(self):
        self.codigo = None
        self.nome = None
        self.agencia = None
        self.conta = None
        self.codigo_cliente = None

    
    @abstractmethod
    def cadastro_bancario():
        pass