from django.shortcuts import render
from .services.dashboard import DashboardService
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse


@login_required(redirect_field_name='login')
def return_dashboard(request):
    return render(request, 'dashboard/dashboard.html', {'nomes': "", 'dados_json': ""})


@login_required(redirect_field_name='login')
def retorna_dados_dashboard(request):

    if request.method == 'POST':
        try:
            
            #Athenas
            dados_athenas = processa_dados_pagamentos_financeiros_dash_athenas()
            
            #Irko
            dados_irko = processa_dados_pagamentos_financeiros_dash_irko()

            #Consolida dados Athenas x Irko
            dados_consolidados = consolida_dados_athenas_irko(dados_athenas,dados_irko)

            if dados_consolidados['success']:
                return JsonResponse(dados_consolidados, safe=False, status=200)
            else:
                return JsonResponse({'error': "Não foi possível carregar dados"}, safe=False, status=500)

        except Exception as e:
            return JsonResponse({'error': str("Não foi possível carregar dados")}, status=500)
    else:
        return HttpResponse(status=405) 

def processa_dados_pagamentos_financeiros_dash_athenas():
    
        try:
            # Chama lógica de negócio
            dados_athenas = DashboardService()
            return dados_athenas.recupera_pagamentos_athenas()
            
        except Exception as e:
            return {'data': {'code': 500, 'message': 'Não foi possível retornar dados.'}, 'success': False}


def processa_dados_pagamentos_financeiros_dash_irko():
    
        try:
            # Chama lógica de negócio
            dados_irko = DashboardService()
            return dados_irko.recupera_pagamentos_irko()
            
        except Exception as e:
            return {'data': {'code': 500, 'message': 'Não foi possível retornar dados.'}, 'success': False}


def consolida_dados_athenas_irko(dados_athenas,dados_irko):
    
        try:
            # Chama lógica de negócio
            dados_combinados = DashboardService()
            return dados_combinados.combina_dados_athenas_irko(dados_athenas,dados_irko)
            
        except Exception as e:
            print(e)
            return {'data': {'code': 500, 'message': 'Não foi possível retornar dados.'}, 'success': False}
        

@login_required(redirect_field_name='login')
def retorna_dados_doctos_indefinidos(request):

    if request.method == 'POST':
        try:
            
            #Athenas
            dados_athenas = processa_dados_doctos_indefinidos_athenas()
            #Irko
            dados_irko = processa_dados_doctos_indefinidos_irko()

            #Consolida dados Athenas x Irko
            dados_consolidados = consolida_doctos_indefinidos_athenas_irko(dados_athenas,dados_irko)

            if dados_consolidados['success']:
                return JsonResponse(dados_consolidados, safe=False, status=200)
            else:
                return JsonResponse({'error': "Não foi possível carregar dados"}, safe=False, status=500)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str("Não foi possível carregar dados")}, status=500)
    else:
        return HttpResponse(status=405) 


def processa_dados_doctos_indefinidos_irko():
    
        try:
            # Chama lógica de negócio
            dados_irko = DashboardService()
            return dados_irko.recupera_doctos_indenifidos_irko()
            
        except Exception as e:
            return {'data': {'code': 500, 'message': 'Não foi possível retornar dados.'}, 'success': False}
        

def processa_dados_doctos_indefinidos_athenas():
    
        try:
            # Chama lógica de negócio
            dados_athenas = DashboardService()
            return dados_athenas.recupera_doctos_indefinidos_athenas()
            
        except Exception as e:
            print(e)
            return {'data': {'code': 500, 'message': 'Não foi possível retornar dados.'}, 'success': False}
        

def consolida_doctos_indefinidos_athenas_irko(dados_athenas,dados_irko):
    
        try:
            # Chama lógica de negócio
            dados_combinados = DashboardService()
            return dados_combinados.combina_dados_doctos_athenas_irko(dados_athenas,dados_irko)
            
        except Exception as e:
            print(e)
            return {'data': {'code': 500, 'message': 'Não foi possível retornar dados.'}, 'success': False}


@login_required(redirect_field_name='login')
def retorna_ranking_doctos_indefinidos(request):

    if request.method == 'POST':
        try:
            
            #Athenas
            dados_athenas = processa_ranking_doctos_indefinidos_athenas()
            
            #Irko
            #dados_irko = processa_dados_pagamentos_financeiros_dash_irko()

            #Consolida dados Athenas x Irko
            #dados_consolidados = consolida_dados_athenas_irko(dados_athenas,dados_irko)

            if dados_athenas['success']:
                return JsonResponse(dados_athenas, safe=False, status=200)
            else:
                return JsonResponse({'error': "Não foi possível carregar dados"}, safe=False, status=500)

        except Exception as e:
            return JsonResponse({'error': str("Não foi possível carregar dados")}, status=500)
    else:
        return HttpResponse(status=405)
    


def processa_ranking_doctos_indefinidos_athenas():
    
        try:
            # Chama lógica de negócio
            dados_athenas = DashboardService()
            return dados_athenas.recupera_ranking_doctos_indefinidos_athenas()
            
        except Exception as e:
            return {'data': {'code': 500, 'message': 'Não foi possível retornar dados.'}, 'success': False}