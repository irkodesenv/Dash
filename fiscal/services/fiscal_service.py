from .fiscal import Fiscal


class FiscalAthenas(Fiscal):
    
    def __init__(self, conexao_bd):
        self.conexao_bd = conexao_bd
        

    def retorna_qtd_entrada_saida_produto(self, data_ini, data_fim, codigo_empresa):
        """
        Retorna a quantidade de movimentações de entrada e saída de produtos e serviços em um determinado período, opcionalmente filtrada por código de empresa.

        A consulta agrupa os dados por tipo de movimentação (entrada ou saída) e por produto ou serviço.

        Args:
            data_ini (str): Data de início do período no formato 'YYYY-MM-DD'.
            data_fim (str): Data de fim do período no formato 'YYYY-MM-DD'.
            codigo_empresa (str): Código(s) da empresa para filtrar os dados. Pode ser uma string de múltiplos códigos separados por vírgula.

        Returns:
            list: Uma lista de dicionários contendo o tipo de movimentação e a quantidade associada.
            Em caso de erro, retorna {"Erro": 0}.

        Raises:
            Exception: Captura exceções que possam ocorrer durante a execução da consulta ao banco de dados e retorna {"Erro": 0}.
        """

        try:        
            where_clause = f"es.TIPO IN ('E', 'S') AND DATAMOVIMENTO BETWEEN '{data_ini}' AND '{data_fim}'"     
            if codigo_empresa:
                where_clause += f" AND es.CODIGOEMPRESA in ({codigo_empresa})" 

            data = self.conexao_bd.select("TABENTRADASAIDA es") \
                                .joins("INNER JOIN TABMOVPRODUTOS mp ON (es.IDMASTER = mp.IDMASTER)")\
                                .where(where_clause) \
                                .values("CASE \
                                            WHEN es.TIPO = 'E' AND COALESCE(mp.SERVICO, 0) = 0 THEN 'Entradas (Produto)' \
                                            WHEN es.TIPO = 'S' AND COALESCE(mp.SERVICO, 0) = 0 THEN 'Saidas (Produto)' \
                                            WHEN es.TIPO = 'E' AND COALESCE(mp.SERVICO, 0) = 1 THEN 'Entradas (Serviço)' \
                                            WHEN es.TIPO = 'S' AND COALESCE(mp.SERVICO, 0) = 1 THEN 'Saidas (Serviço)' \
                                            ELSE mp.SERVICO \
                                        END AS tipo_movimento, \
                                        COUNT(*) AS quantidade"
                                        ) \
                                .group_by("es.TIPO, mp.SERVICO") \
                                .execute()
            return data
        except Exception as e:
            return {"Erro": 0}
        
        
    def retorna_qtd_importacoes(self, data_ini, data_fim, codigo_empresa):
        """
        Retorna a quantidade de importações registradas em um determinado período, opcionalmente filtrada por código de empresa.

        Args:
            data_ini (str): Data de início do período no formato 'YYYY-MM-DD'.
            data_fim (str): Data de fim do período no formato 'YYYY-MM-DD'.
            codigo_empresa (str): Código(s) da empresa para filtrar os dados. Pode ser uma string de múltiplos códigos separados por vírgula.

        Returns:
            int: Quantidade de importações no período especificado. Retorna 0 em caso de erro.

        Raises:
            Exception: Captura exceções que possam ocorrer durante a execução da consulta ao banco de dados e retorna 0.
        """
        try:        
            where_clause = f"LPAD(mp.SITUACAOTRIBUTARIA,1) IN (1,2) AND es.TIPO = 'E' AND DATAMOVIMENTO BETWEEN '{data_ini}' AND '{data_fim}'"     
            if codigo_empresa:
                where_clause += f" AND es.CODIGOEMPRESA in ({codigo_empresa})" 

            data = self.conexao_bd.select("TABENTRADASAIDA es") \
                                .joins("INNER JOIN TABMOVPRODUTOS mp ON (es.IDMASTER = mp.IDMASTER)")\
                                .where(where_clause) \
                                .values("COALESCE(COUNT(es.CODIGOEMPRESA),0)") \
                                .group_by("es.CODIGOEMPRESA") \
                                .execute()
            return data[0][0]
        except Exception as e:
            return 0  
        
        
    def retorna_qtd_filiais(self, data_fim, codigo_empresa):
        """
            Retorna a quantidade de filiais registradas até uma data específica, opcionalmente filtrada por código de empresa.

            Args:
                data_fim (str): Data de fim do período no formato 'YYYY-MM-DD'.
                codigo_empresa (str): Código(s) da empresa para filtrar os dados. Pode ser uma string de múltiplos códigos separados por vírgula.

            Returns:
                int: Quantidade de filiais até a data especificada. Retorna 0 em caso de erro.

            Raises:
                Exception: Captura exceções que possam ocorrer durante a execução da consulta ao banco de dados e retorna 0.
        """
        try:        
            where_clause = f"CODIGO > 1 AND DTREG <= '{data_fim}'"     
            if codigo_empresa:
                where_clause += f" AND CODIGOEMPRESA in ({codigo_empresa})" 
                
            data = self.conexao_bd.select("TABFILIAL") \
                                .where(where_clause) \
                                .values("count(CODIGO)") \
                                .execute()
            return data[0][0]
        except Exception as e:
            return 0  