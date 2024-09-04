from django.urls import path
from . import views

app_name = 'relatorios_financeiro'
urlpatterns = [
    path('',views.retorna_relatorio_financeiro,name='rel_financeiro')
]