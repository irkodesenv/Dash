from django.shortcuts import render

def return_dashboard(request):
    return render(request, 'dashboard/dashboard.html', {'nomes': "", 'dados_json': ""})