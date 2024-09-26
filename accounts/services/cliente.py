from .pessoa import Pessoa


class Cliente(Pessoa):
    
    def lista_cadastros(self):
        try:
            data = self.conexao.select("IRK_SYS_EMPIRK irk") \
                                .joins("LEFT JOIN TABFILIAL tf ON tf.CODIGOEMPRESA = irk.CODEMP AND tf.CODIGO = 1")\
                                .values("DISTINCT CODEMP, tf.nome, tf.CNPJ")\
                                .execute()

            return data
        except Exception as e:
            raise RuntimeError("Erro ao consultar clientes: " + str(e))