from .pessoa import Pessoa

class Funcionario(Pessoa):
    
    def lista_cadastros(self):
        pass
    
    
    def conta_tipo_funcionario(self, tipos, data_fim, codigo_empresa, codigo_filial):
        where_clause = f"TIPO in {tipos} AND DATACADASTRO <= '{data_fim}' and SITUACAO = 1"
        if codigo_empresa:
            where_clause += f" AND CODIGOEMPRESA = {codigo_empresa}"
        
        if codigo_filial:
            where_clause += f" AND CODIGOFILIAL = {codigo_filial}"

        data = (
            self.conexao.select('TABPESSOAS')
            .where(where_clause)
            .values("CASE WHEN TIPO = 'O' THEN 'Pró Labore' WHEN TIPO = 'N' THEN 'Funcionários CLT' WHEN TIPO = 'M' THEN 'Autônomos' END AS TIPO, COUNT(CODIGO)")
            .group_by("TIPO")
            .execute()
        )

        return dict((item[0].strip(), item[1]) for item in data) if data else {}


    def contar_estagiarios(self, data_fim, codigo_empresa, codigo_filial):
        where_clause = f"ESTAGIARIO = 1 AND TIPO = 'O' AND DATACADASTRO <= '{data_fim}' and SITUACAO = 1"
        if codigo_empresa:
            where_clause += f" AND CODIGOEMPRESA = {codigo_empresa}"

        data = (
            self.conexao.select('TABPESSOAS')
            .where(where_clause)
            .values("COUNT(CODIGO)")
            .execute()
        )

        return data[0][0] if data else 0


    def contar_admissoes(self, data_ini, data_fim, codigo_empresa, codigo_filial):
        where_clause = f"DATACADASTRO BETWEEN '{data_ini}' AND '{data_fim}' AND TIPO = 'N' and SITUACAO = 1"
        if codigo_empresa:
            where_clause += f" AND CODIGOEMPRESA = {codigo_empresa}"

        data = (
            self.conexao.select('TABPESSOAS')
            .where(where_clause)
            .values("COUNT(CODIGO)")
            .execute()
        )

        return data[0][0] if data else 0


    def contar_demissoes(self, data_ini, data_fim, codigo_empresa, codigo_filial):
        where_clause = f"DATADEMISSAO BETWEEN '{data_ini}' AND '{data_fim}' AND TIPO = 'N'"
        if codigo_empresa:
            where_clause += f" AND CODIGOEMPRESA = {codigo_empresa}"

        data = (
            self.conexao.select('TABPESSOAS')
            .where(where_clause)
            .values("COUNT(CODIGO)")
            .execute()
        )

        return data[0][0] if data else 0