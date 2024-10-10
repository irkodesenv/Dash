from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.auth_login, name='login'),
    path('accounts/login/', views.auth_login, name='login'),
    path('logoff/', views.logoff, name='logoff'),
]