from ..cliente import Cliente
from typing import List, Dict, Any, Tuple

class ClienteService:
    
    def __init__(self, conexao):
        self.conexao = conexao
        self.cliente = Cliente(self.conexao)
    
    
    def obter_clientes(self) -> List[Tuple[Any, Any, Any]]:
        """
            Retorna uma lista de cadastros de clientes.

            Parâmetros:
                -

            Retorno:
                List[Tuple[Any, Any, Any]]: Retorna uma lista

            Exceções:
                -

            Exemplo de uso:
                >> obj = ExemploClasse()
                >> obj.obter_clientes()                
        """
        return self.cliente.lista_cadastros()
    
    
    def obter_descendentes(self, codigo_cliente: int) -> List[Tuple[Any]]:    
        """
            Obtém e formata uma lista de descendentes de um cliente específico.

            Parâmetros:
                codigo_cliente (int): codigo do cliente. 

            Retorno:
                List: Lista de descendentes ou array vazio

            Exceções:
                -

            Exemplo de uso:
                >> obj = ExemploClasse()
                >> obj.obter_descendentes(12345)               
        """
        descendentes = self.cliente.lista_cadastro_descendentes(codigo_cliente)   
        return self.formata_dados_clientes_formulario(descendentes)

    
    def formata_dados_clientes_formulario(self, clientes: List[Tuple[Any]]) -> List[Dict[str, Any]]:
        """
            Formata uma lista de dados de clientes para um formato específico adequado a formulários.

            A função recebe uma lista de tuplas que contém informações de clientes e converte cada tupla 
            em um dicionário com chaves específicas: 'Codigo', 'CNPJ' e 'Razao'. Apenas as tuplas que possuem 
            todos os três valores (não nulos ou vazios) são processadas e incluídas na lista final de dicionários.

            Parâmetros:
                clientes (List[Tuple[Any, Any, Any]]): Uma lista de tuplas, onde cada tupla representa um cliente e 
                contém três elementos:
                    - O primeiro elemento representa o código do cliente.
                    - O segundo elemento representa a razão social do cliente.
                    - O terceiro elemento representa o CNPJ do cliente.
            
            Retorno:
                List[Dict[str, Any]]: Uma lista de dicionários, onde cada dicionário possui as chaves 'Codigo', 'CNPJ' 
                e 'Razao', representando as informações do cliente formatadas para serem usadas em um formulário.

            Exceções:
                -

            Exemplo de uso:
                >> obj = ExemploClasse()
                >> clientes = [(123, 'Empresa X', '12.345.678/0001-99'), (456, 'Empresa Y', '98.765.432/0001-11')]
                >> obj.formata_dados_clientes_formulario(clientes)
                [{'Codigo': 123, 'Razao': 'Empresa X', 'CNPJ': '12.345.678/0001-99'}, {'Codigo': 456, 'Razao': 'Empresa Y', 'CNPJ': '98.765.432/0001-11'}]
        """
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
        """
            Obtém e formata uma lista de clientes para uso em um formulário.

            A função primeiro invoca `obter_clientes` para recuperar uma lista de clientes e, em seguida, 
            formata esses dados utilizando a função `formata_dados_clientes_formulario`, retornando a lista 
            de clientes já formatada. O formato resultante é uma lista de dicionários, com chaves específicas 
            como 'Codigo', 'CNPJ' e 'Razao'.

            Parâmetros:
                -

            Retorno:
                List[Dict[str, Any]]: Uma lista de dicionários, onde cada dicionário contém informações formatadas 
                dos clientes, como 'Codigo', 'CNPJ', e 'Razao', para serem usados em um formulário.

            Exceções:
                -

            Exemplo de uso:
                >> obj = ExemploClasse()
                >> obj.obter_clientes_formatados_formulario()
                [{'Codigo': 123, 'Razao': 'Empresa X', 'CNPJ': '12.345.678/0001-99'}, {'Codigo': 456, 'Razao': 'Empresa Y', 'CNPJ': '98.765.432/0001-11'}]
        """
        clientes = self.obter_clientes()
        return self.formata_dados_clientes_formulario(clientes)
