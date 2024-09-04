import fdb
from django.conf import settings

class Conexao:    

    def __init__(self):
        self.host = settings.HOST
        self.database = settings.DATABASE
        self.port = settings.PORT
        self.user = settings.USER
        self.password = settings.PASSWORD


    def connect_db_firebird(self):
        self.conexao = fdb.connect(
            host = self.host, 
            database = self.database, 
            port = self.port,
            user = self.user, 
            password = self.password
        )
        
        return self.conexao


    def select(self, tabela):
        return QueryBuilder(self.connect_db_firebird(), tabela)


class QueryBuilder:

    def __init__(self, conn, tabela):
        self.conn = conn
        self.values_prop = None
        self.tabela = tabela
        self.joins = None
        self.where_clause = None
        self.group_by = None
        self.order_by = None


    def joins(self, joins):
        """
            Define a cláusula JOIN da consulta.

            Args:
            - joins (str): Cláusula JOIN.

            Exemplo de uso:
                data = conexao_bd.select("TABELA1 a")
                 .joins("[INNER, RIGTH, LEFT...etc] JOIN TABELA2 b ON a.departamento_id = b.id")
                 .execute()

            Returns:
            - QueryBuilder: Instância do QueryBuilder para encadeamento.
        """

        self.joins = joins
        return self


    def where(self, where):
        """
            Define a cláusula WHERE da consulta.

            Args:
            - where (str): Condição da cláusula WHERE.

            Exemplo de uso:
                data = conexao_bd.select("TABELA1")
                 .where("nome = 'João'")
                 .execute()

            Returns:
            - QueryBuilder: Instância do QueryBuilder para encadeamento.
        """

        self.where_clause = where
        return self
    

    def values(self, values):
        """
            Define as colunas da tabela que serão retornadas

            Args:
            - values (str): Coluna(s) para retorno.

            Exemplo de uso:
                data = conexao_bd.select("TABELA1")
                    values("XXXXXXX, XXXXXXX, XXXXXXXX").execute()

            Returns:
            - QueryBuilder: Instância do QueryBuilder para encadeamento.
        """
        barra_invertida = '                                     '
        self.values_prop = values.replace(barra_invertida, ' ')
        return self


    def group_by(self, group):
        """
            Define a cláusula GROUP BY da consulta.

            Args:
            - group (str): Coluna(s) para agrupamento.
            
            Exemplo de uso:
                data = conexao_bd.select("TABELA1 u")
                    .group by("u.nome")
                    .execute()

            Returns:
            - QueryBuilder: Instância do QueryBuilder para encadeamento.
        """

        self.group_by = group
        return self


    def order_by(self, orders):
        """
            Define a cláusula ORDER BY da consulta.

            Args:
            - orders (str): Coluna(s) para ordenação.

            Exemplo de uso:
                data = conexao_bd.select("TABELA1 u")
                    .order_by("u.nome ASC")
                    .execute()

            Returns:
            - QueryBuilder: Instância do QueryBuilder para encadeamento.
        """

        self.order_by = orders
        return self


    def execute(self):
        try:
            # Construção da consulta SQL baseada nos parâmetros fornecidos
            sql = f"SELECT {self.values_prop.strip() if self.values_prop else "*"} FROM {self.tabela.strip()}"

            if self.joins:
                sql += f" {self.joins.strip()}"
            if self.where_clause:
                sql += f" WHERE {self.where_clause.strip()}"
            if self.group_by:
                sql += f" GROUP BY {self.group_by.strip()}"
            if self.order_by:
                sql += f" ORDER BY {self.order_by.strip()}"

            cursor = self.conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()

            return rows

        except fdb.Error as e:
            return {f"Erro ao executar consulta SQL: {e}"}

        finally:
            cursor.close()
