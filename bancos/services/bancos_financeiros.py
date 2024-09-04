from .banco import IBanco
from conexoes.services.firebird import Conexao


class BancoFinanceiro(IBanco):

    def __init__(self):
        super().__init__()
        self.conexao = Conexao()
    
    
    def cadastro_bancario(self):
        pass


    def retorna_contagem_bancos(self):
        where = self._where_codigo_cliente()

        data = self.conexao.select("TABCONTABANCARIA cb") \
                                    .joins("LEFT JOIN IRK_SYS_EMPIRK irk_sys ON cb.CODIGOEMPRESA = IRK_SYS.CODEMP \
                                        INNER JOIN TABCODIGOBANCO cod_b ON cb.CODIGOBANCO = cod_b.CODIGO AND cod_b.CODIGO <> 'n/a'\
                                        ")\
                                    .values("LPAD(CAST(cb.CODIGOBANCO AS VARCHAR(10)), 3, '0'), \
                                            COUNT(cb.CODIGOBANCO), \
                                            COUNT(DISTINCT cb.CODIGOEMPRESA) AS TOTAL_CLIENTES,\
                                            COD_B.NOME"
                                    )\
                                    .where("CODIGOBANCO IS NOT NULL AND CODIGOBANCO <> 000 and CODIGOBANCO <> 999 " + where )\
                                    .group_by("LPAD(CAST(cb.CODIGOBANCO AS VARCHAR(10)), 3, '0'), 4")\
                                    .execute()
        return data
    

    def _where_codigo_cliente(self):
        if self.codigo_cliente:
            return f"and IRK_SYS.CODEMP in ({self.codigo_cliente})"
        return ""