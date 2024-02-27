from django.urls import path
from . import views

urlpatterns = [
    path('', views.test),
    path('apps/', views.returnApps),
    path('progs/', views.returnProgCodes),
]