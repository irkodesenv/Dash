from .clientes import Cliente
from conexoes.services.firebird import Conexao


class ClienteAthenas(Cliente):

    def __init__(self):       
        super().__init__()  # Chama o construtor da classe pai (Cliente)
        self.conexao = Conexao()


    def retorna_cadastro(self):
        where = self._where_codigo_cliente()
  
        try:
            data = self.conexao.select("IRK_SYS_EMPIRK irk") \
                                .joins("LEFT JOIN TABFILIAL tf ON tf.CODIGOEMPRESA = irk.CODEMP AND tf.CODIGO = 1")\
                                .values("DISTINCT CODEMP, tf.nome, tf.CNPJ")\
                                .where(where)\
                                .execute()

            return data
        except Exception as e:
            raise RuntimeError("Erro ao consultar clientes: " + str(e))
        

    def _where_codigo_cliente(self):
        if self.codigo_cliente:
            return f"irk.CODEMP in({self.codigo_cliente})"
        return ""