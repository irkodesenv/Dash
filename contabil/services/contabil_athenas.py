from .contabil import Contabil


class ContabilAthenas(Contabil):
    
    def __init__(self, conexao_bd):
        self.conexao_bd = conexao_bd
    
    
    def retorna_qtd_lctos_contabeis(self, data_ini, data_fim, codigo_empresa, codigo_filial):
        """
            Retorna a quantidade de lançamentos contábeis registrados em um determinado período, opcionalmente filtrada por código de empresa.

            Args:
                data_ini (str): Data de início do período no formato 'YYYY-MM-DD'.
                data_fim (str): Data de fim do período no formato 'YYYY-MM-DD'.
                codigo_empresa (str): Código(s) da empresa para filtrar os dados. Pode ser uma string de múltiplos códigos separados por vírgula.

            Returns:
                int: Quantidade de lançamentos contábeis no período especificado. Retorna 0 em caso de erro.

            Raises:
                Exception: Captura exceções que possam ocorrer durante a execução da consulta ao banco de dados e retorna 0.
        """ 
        try:                   
            where_clause = f"lnc.DATAREGISTRO BETWEEN '{data_ini}' AND '{data_fim}'"

            if codigo_empresa:
                where_clause += f" AND ltc.CODIGOEMPRESA in ({codigo_empresa})"
            
            if codigo_filial:
                where_clause += f" AND ltc.CODIGOFILIAL in ({codigo_filial})"

            data = self.conexao_bd.select("TABLOTECONTABIL ltc") \
                                .joins("INNER JOIN TABLNCCONTABEIS lnc ON ltc.IDMASTER = lnc.IDMASTER")\
                                .where(where_clause) \
                                .values("COUNT(ltc.CODIGOEMPRESA)") \
                                .execute()
            return data[0][0]
        except Exception as e:
            return 0
    
    
    def retorna_qtd_partidas_contabeis(self, data_ini, data_fim, codigo_empresa, codigo_filial):
        """
            Retorna a quantidade de partidas contábeis registradas em um determinado período e opcionalmente filtradas por código de empresa.

            Args:
                data_ini (str): Data de início do período no formato 'YYYY-MM-DD'.
                data_fim (str): Data de fim do período no formato 'YYYY-MM-DD'.
                codigo_empresa (str): Código(s) da empresa para filtrar os dados. Pode ser uma string de múltiplos códigos separados por vírgula.

            Returns:
                int: Quantidade de partidas contábeis no período especificado. Retorna 0 em caso de erro.

            Raises:
                Exception: Captura exceções que possam ocorrer durante a execução da consulta ao banco de dados e retorna 0.
        """
        try:                    
            where_clause = f"lnc.DATAREGISTRO BETWEEN '{data_ini}' AND '{data_fim}'"

            if codigo_empresa:
                where_clause += f" AND ltc.CODIGOEMPRESA in ({codigo_empresa})" 
                
            if codigo_filial:
                where_clause += f" AND ltc.CODIGOFILIAL in ({codigo_filial})"

            data = self.conexao_bd.select("TABLOTECONTABIL ltc") \
                                .joins("INNER JOIN TABLNCCONTABEIS lnc ON ltc.IDMASTER = lnc.IDMASTER \
                                        INNER JOIN TABLNCCONTABEISDETALHE lncd ON lnc.IDMASTER = lncd.IDMASTER"
                                    )\
                                .where(where_clause) \
                                .values("COUNT(ltc.CODIGOEMPRESA)") \
                                .execute()
            return data[0][0]
        except Exception as e:
            return 0
        
        
    def retorna_qtd_ativo_imobilizado(self, data_ini, data_fim, codigo_empresa, codigo_filial):
        """
            Retorna a quantidade de ativos imobilizados adquiridos em um determinado período, opcionalmente filtrada por código de empresa.

            Args:
                data_ini (str): Data de início do período de aquisição no formato 'YYYY-MM-DD'.
                data_fim (str): Data de fim do período de aquisição no formato 'YYYY-MM-DD'.
                codigo_empresa (str): Código(s) da empresa para filtrar os dados. Pode ser uma string de múltiplos códigos separados por vírgula.

            Returns:
                int: Quantidade de ativos imobilizados adquiridos no período especificado. Retorna 0 em caso de erro.

            Raises:
                Exception: Captura exceções que possam ocorrer durante a execução da consulta ao banco de dados e retorna 0.
        """
        try:                    
            where_clause = f"DTAQUISICAO BETWEEN '{data_ini}' AND '{data_fim}'"

            if codigo_empresa:
                where_clause += f" AND CODIGOEMPRESA in ({codigo_empresa})"
            
            if codigo_filial:
                where_clause += f" AND CODIGOFILIAL in ({codigo_filial})" 

            data = self.conexao_bd.select("TABATIVOIMOBILIZADO") \
                                .joins("INNER JOIN TABLNCCONTABEIS lnc ON ltc.IDMASTER = lnc.IDMASTER \
                                        INNER JOIN TABLNCCONTABEISDETALHE lncd ON lnc.IDMASTER = lncd.IDMASTER"
                                    )\
                                .where(where_clause) \
                                .values("COUNT(CODIGOEMPRESA)") \
                                .execute()
            return data[0][0]
        except Exception as e:
            return 0