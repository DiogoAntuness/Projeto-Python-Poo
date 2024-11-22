# adote/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.pagina_inicial, name='pagina_inicial'),

    path('lista_animais', views.lista_animais, name='lista_animais'),
    path('animal/<int:animal_id>/', views.detalhes_animal, name='detalhes_animal'),

    # URLs para login, logout e registro
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('registro/', views.registro, name='registro'),

    # URL para adotar um animal
    path('adotar/<int:animal_id>/', views.adotar_animal, name='adotar_animal'),
    #URL p/ doar
    path('doar/', views.doar_animal, name='doar_animal'),
]
