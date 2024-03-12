from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name = 'register'), 
    path('log-in/', views.loginAuth, name = 'log-in'), 
    path('log-out/', views.logOut, name = 'log-out'), 
    path('delete/', views.deleteCity, name = 'delete'), 
]