from django.test import TestCase
from unittest.mock import patch, MagicMock
from contabil.services.contabil_athenas import ContabilAthenas  # Substitua pelo caminho correto

class RetornaQtdLctosContabeisTestCase(TestCase):

    def test_retorna_qtd_lctos_contabeis_com_codigo_empresa(self):
        """
        Testa o retorno da quantidade de lançamentos contábeis com um código de empresa específico.
        """
        # Criando um mock para o banco de dados
        mock_conexao_bd = MagicMock()

        # Configurando o mock
        mock_select = MagicMock()
        mock_conexao_bd.select.return_value = mock_select
        mock_select.joins.return_value = mock_select
        mock_select.where.return_value = mock_select
        mock_select.values.return_value = mock_select
        mock_select.execute.return_value = [(5,)] # Simulando o retorno de 5

        obj = ContabilAthenas(conexao_bd=mock_conexao_bd)
        
        # Chamando o método a ser testado
        resultado = obj.retorna_qtd_lctos_contabeis('2024-01-01', '2024-12-31', '123')

        # Verificando o resultado
        self.assertEqual(resultado, 5)

        # Verificando se a query foi executada corretamente
        mock_conexao_bd.select.assert_called_once_with('TABLOTECONTABIL ltc')
        mock_select.joins.assert_called_once_with("INNER JOIN TABLNCCONTABEIS lnc ON ltc.IDMASTER = lnc.IDMASTER")
        mock_select.where.assert_called_once_with(
            "lnc.DATAREGISTRO BETWEEN '2024-01-01' AND '2024-12-31' AND ltc.CODIGOEMPRESA in (123)"
        )
        mock_select.values.assert_called_once_with("COUNT(ltc.CODIGOEMPRESA)")


    def test_retorna_qtd_lctos_contabeis_sem_codigo_empresa(self):
        """
        Testa o retorno da quantidade de lançamentos contábeis sem um código de empresa específico.
        """
        # Criando um mock para o banco de dados
        mock_conexao_bd = MagicMock()

        # Configurando o mock
        mock_select = MagicMock()
        mock_conexao_bd.select.return_value = mock_select
        mock_select.joins.return_value = mock_select
        mock_select.where.return_value = mock_select
        mock_select.values.return_value = mock_select
        mock_select.execute.return_value = [(10,)]  # Simulando o retorno de 10

        # Instanciando a classe com o mock do banco de dados
        obj = ContabilAthenas(conexao_bd=mock_conexao_bd)
        
        # Chamando o método a ser testado
        resultado = obj.retorna_qtd_lctos_contabeis('2024-01-01', '2024-12-31', None)

        # Verificando o resultado
        self.assertEqual(resultado, 10)

        # Verificando se a query foi executada corretamente
        mock_conexao_bd.select.assert_called_once_with('TABLOTECONTABIL ltc')
        mock_select.joins.assert_called_once_with("INNER JOIN TABLNCCONTABEIS lnc ON ltc.IDMASTER = lnc.IDMASTER")
        mock_select.where.assert_called_once_with("lnc.DATAREGISTRO BETWEEN '2024-01-01' AND '2024-12-31'")
        mock_select.values.assert_called_once_with("COUNT(ltc.CODIGOEMPRESA)")


    def test_retorna_qtd_lctos_contabeis_com_erro(self):
        """
        Testa o comportamento da função ao ocorrer uma exceção durante a execução da consulta ao banco de dados.
        """
        # Criando um mock para o banco de dados
        mock_conexao_bd = MagicMock()

        # Configurando o mock
        mock_conexao_bd.select.side_effect = Exception("Erro de banco de dados")

        obj = ContabilAthenas(conexao_bd=mock_conexao_bd)
        
        # Chamando o método a ser testado
        resultado = obj.retorna_qtd_lctos_contabeis('2024-01-01', '2024-12-31', '123')

        # Verificando se o resultado retornado é 0 em caso de exceção
        self.assertEqual(resultado, 0)

        # Verificando se a query foi chamada antes do erro
        mock_conexao_bd.select.assert_called_once_with('TABLOTECONTABIL ltc')
