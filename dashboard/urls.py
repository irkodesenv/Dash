from django.urls import path
from django.contrib import admin
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.return_dashboard, name="dashboard")
]