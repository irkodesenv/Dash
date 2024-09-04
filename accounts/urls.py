from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.login, name='login'),
    path('accounts/login/', views.login, name='login'),
    path('logoff/', views.logoff, name='logoff'),
]