from abc import ABC, abstractmethod

class Pessoa(ABC):
    
    def __init__(self, conexao):
        self.conexao = conexao
        
    @abstractmethod
    def lista_cadastros(self):
        pass