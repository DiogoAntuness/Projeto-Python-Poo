from django import forms
from .models import Animal
from adote.models import Usuario
from django.contrib.auth.forms import UserCreationForm

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome', 'idade_meses', 'idade_anos', 'sexo', 'tipo', 'local', 'descricao']

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2', 'tipo_usuario', 'telefone']

class RegistroForm(UserCreationForm): 
    class Meta: 
        model = Usuario 
        fields = ['username', 'password1', 'password2', 'tipo_usuario', 'telefone']
     
