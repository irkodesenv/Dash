from django.shortcuts import render
from .services.controller_irko import ControllerClienteIrko


def clientes(request):
    pass


def retorna_cadastro_clientes():
    try:
        cliente = ControllerClienteIrko()    
        return cliente.retorna_cadastro_clientes()
    except Exception as e:        
        #logger.error(f"Erro ao processar relatório: {str(e)}")
        return {'data': {'code': 500, 'message': 'Não foi possível retornar dados.'}, 'success': False}