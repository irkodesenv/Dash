from datetime import datetime

def converte_array_data_para_sistema(arr_data):
    datas_convertidas = []

    for data_str in arr_data:
        data_obj = datetime.strptime(data_str, '%d/%m/%Y')
        data_formatada = data_obj.strftime('%Y-%m-%d')
        datas_convertidas.append(data_formatada)

    return datas_convertidas