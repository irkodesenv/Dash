from .pessoa import Pessoa
from typing import List, Dict, Any, Tuple


class Cliente(Pessoa):
    
    def lista_cadastros(self) -> List[Tuple[int, str, str]]:
        """
            Recupera uma lista de cadastro de clientes IRKO.
            
            Retorno:           
                List[Tuple[int, str, str]]
                    Uma lista de tuplas, onde cada tupla contém três elementos:
                    - int: O código da empresa.
                    - str: O nome da empresa.
                    - str: O CNPJ da empresa.
            
            Exceções:           
                RuntimeError:
                    Lançada se houver um erro ao consultar os clientes. A mensagem da exceção contém detalhes adicionais sobre o erro.
                    
            Exemplo:
                self.cliente = Cliente(self.conexao)              
                clientes = self.cliente.lista_cadastros()
                
                for codigo, nome, cnpj in filiais:
                    print(f"Filial: {codigo}, Nome: {nome}, CNPJ: {cnpj}")        
        """
        try:
            data = self.conexao.select("IRK_SYS_EMPIRK irk") \
                                .joins("LEFT JOIN TABFILIAL tf ON tf.CODIGOEMPRESA = irk.CODEMP AND tf.CODIGO = 1")\
                                .values("DISTINCT CODEMP, tf.nome, tf.CNPJ")\
                                .execute()

            return data
        except Exception as e:
            raise RuntimeError("Erro ao consultar clientes: " + str(e))
        
        
    def lista_cadastro_descendentes(self, codigo_cliente: int) -> List[Tuple[int, str, str]]:
        """
            Recupera uma lista de filiais associadas a um cliente específico a partir da tabela TABFILIAL.

            Parâmetros:           
                codigo_cliente : int
                    O código único que identifica o cliente (empresa) cujas filiais estão sendo consultadas.

            Retorno:           
                List[Tuple[int, str, str]]
                    Uma lista de tuplas, onde cada tupla contém três elementos:
                    - int: O código da filial.
                    - str: O nome da filial.
                    - str: O CNPJ da filial.

            Exceções:           
                RuntimeError:
                    Lançada se houver um erro ao consultar os clientes. A mensagem da exceção contém detalhes adicionais sobre o erro.

            Exemplo:
                codigo_cliente = 123
                filiais = obj.lista_cadastro_descendentes(codigo_cliente)
                for codigo, nome, cnpj in filiais:
                    print(f"Filial: {codigo}, Nome: {nome}, CNPJ: {cnpj}")
        """
        try:
            data = self.conexao.select("TABFILIAL") \
                                .values("CODIGO, NOME, CNPJ") \
                                .where(f"CODIGOEMPRESA = {codigo_cliente}") \
                                .execute()                  
            return data   
        except Exception as e:
            raise RuntimeError("Erro ao consultar clientes: " + str(e))