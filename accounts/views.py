from django.shortcuts import render, redirect
from .services.usuario import Usuario
from django.contrib import auth

# Create your views here.

def login(request):

    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    
    usuario = request.POST.get('usuario', "").strip()
    senha = request.POST.get('senha', "")


    usuario = Usuario(usuario = usuario, senha = senha)
    usuario_autenticado = usuario.authenticate()


    if usuario_autenticado:
        auth.login(request, usuario_autenticado)
        return redirect('dashboard:dashboard')
    else:
        return render(request, 'accounts/login.html', {'error': 'Usuário ou senha inválidos'})


def logoff(request):
    auth.logout(request)
    return redirect('accounts:login') 