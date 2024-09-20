from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services.volumetria_athenas import VolumetriaAthenas


@login_required(redirect_field_name='login')
def retorna_volumetria_consumo_cliente(request):
    
    
    obj = VolumetriaAthenas()
    
    data = obj.controllerMetricas()
    
    
    print(data)
    
    
    return render(request, 'dashboards/volumetria_cliente.html')
