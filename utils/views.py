from datetime import datetime

def converte_array_data_para_sistema(arr_data):
    """
        Converte uma lista de datas no formato 'DD/MM/AAAA' para o formato 'AAAA-MM-DD' (ISO).

        A função recebe uma lista de strings que representam datas no formato brasileiro (dia/mês/ano) 
        e as converte para o formato ISO (ano-mês-dia), que é comumente utilizado em bancos de dados 
        e sistemas backend.

        Parâmetros:
            arr_data (list): Lista de strings contendo datas no formato 'DD/MM/AAAA'.
        
        Retorno:
            list: Lista de strings com as datas convertidas para o formato 'AAAA-MM-DD'.

        Exceções:
            - A função espera que as datas estejam no formato correto. Caso contrário, uma exceção `ValueError`
            será levantada ao tentar converter uma data inválida.
        
        Exemplo de uso:
            >> converte_array_data_para_sistema(["10/09/2023", "25/12/2023"])
            saida: ['2023-09-10', '2023-12-25']
    """
    datas_convertidas = []
    
    for data_str in arr_data:
        data_obj = datetime.strptime(data_str, '%d/%m/%Y')
        data_formatada = data_obj.strftime('%Y-%m-%d')
        datas_convertidas.append(data_formatada)

    return datas_convertidas


def media_periodo_range_data(arr_data) -> int:
    """
        Calcula a quantidade de periodo entre duas datas, considerando o período de 11 a 10 do mês seguinte
        no contexto da IRKO (empresa de consultoria). 
        
        O período calculado leva em conta a data inicial e a data final fornecidas em formato de string (YYYY-MM-DD) 
        e retorna o número de periodo inteiros entre elas.

        Parâmetros:
            arr_data (list): Uma lista contendo duas strings no formato 'YYYY-MM-DD', onde:
                - arr_data[0]: data de início do período
                - arr_data[1]: data de fim do período
        
        Retorno:
            int: Número inteiro representando a quantidade de periodo entre as datas, baseado no critério de 
            cálculo que considera o intervalo de 11 de um mês até o dia 10 do mês seguinte.

        Exceções:
            -

        Exemplo de uso:
            >> media_periodo_range_data(["2023-01-11", "2023-03-10"])
            saida: 2
    """
    
    dt_ini = arr_data[0]
    dt_fim = arr_data[1]
    
    mes_ini = int(dt_ini[5:7])
    ano_ini = int(dt_ini[0:4]) 
    
    mes_fim = int(dt_fim[5:7])
    ano_fim = int(dt_fim[0:4])
    
    if ano_ini == ano_fim:
        qtd_meses = mes_fim - mes_ini
        
        if qtd_meses:
            return int(qtd_meses)
        
        return int(qtd_meses + 1)
    else:        
        teste_ini = 12 - mes_ini 
        teste_fim = mes_fim
        
        qtd_meses = teste_fim + teste_ini
        
        if qtd_meses:
            return int(qtd_meses)
        
        return int(qtd_meses + 1)
    