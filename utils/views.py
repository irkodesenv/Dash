from datetime import datetime

def converte_array_data_para_sistema(arr_data):
    datas_convertidas = []
    
    for data_str in arr_data:
        data_obj = datetime.strptime(data_str, '%d/%m/%Y')
        data_formatada = data_obj.strftime('%Y-%m-%d')
        datas_convertidas.append(data_formatada)

    return datas_convertidas


def media_periodo_range_data(arr_data) -> int:
    """
        Funcao criada para verificar a quantidade de periodo IRKO 11 a 10 do mes seguinte
        
        Return: 
            numero inteiro 
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
    