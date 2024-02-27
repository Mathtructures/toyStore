from django.urls import path
from . import  views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('changelang/<str:lang>',views.change_lang,name='change_lang')
]