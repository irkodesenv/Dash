from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='login')
def retorna_volumetria_consumo_cliente(request):
    return render(request, 'dashboards/volumetria_cliente.html')
