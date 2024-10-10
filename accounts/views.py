from django.shortcuts import render, redirect
from django.contrib import auth
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.

def auth_login(request):

    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    
    
    usuario = request.POST.get('usuario', "").strip()
    senha = request.POST.get('senha', "")
    
    
    url = 'http://10.11.100.122:8002/api/login/'
    
    data = {
        'username': usuario,
        'password': senha
    }
    
    response = requests.post(url, data=data)
    response_data = response.json()
    nome = response_data.get("first_name")
    email = response_data.get("email")


    if response.status_code == 200:
        # Autenticar o usuário com o modelo padrão do Django
        user = authenticate(username=usuario, password=senha)

        if user:
            login(request, user)
            return redirect('dashboard:dashboard')
        else:
            user = User.objects.create_user(
                username=usuario,
                password=senha,
                first_name=nome,
                email=email,
                is_active=True
            )
            # Autenticar o novo usuário
            user_auth = authenticate(username=usuario, password=senha)

            if user_auth:
                login(request, user_auth)
                return redirect('dashboard:dashboard')

    if response.status_code == 400 or response.status_code == 401:
        return render(request, 'accounts/login.html', {'error': 'Usuário ou senha inválidos'})    
    

def logoff(request):
    auth.logout(request)
    return redirect('accounts:login') 