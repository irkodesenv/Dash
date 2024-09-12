from django.urls import path
from . import views

app_name = 'bancos'
urlpatterns = [
    path('', views.bancos, name='bancos'),
]