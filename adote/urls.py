# adote/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_animais, name='lista_animais'),
    path('animal/<int:animal_id>/', views.detalhes_animal, name='detalhes_animal'),
]
