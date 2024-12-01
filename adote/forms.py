from django import forms
from .models import Animal
from adote.models import Usuario
from django.contrib.auth.forms import UserCreationForm

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome', 'idade_meses', 'idade_anos', 'sexo', 'tipo', 'local', 'descricao', 'foto']

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2', 'tipo_usuario', 'telefone']

class RegistroForm(UserCreationForm): 
    class Meta: 
        model = Usuario 
        fields = ['username', 'password1', 'password2', 'tipo_usuario', 'telefone']
        labels = { 
            'username': 'Nome de Usuário', 'password1': 'Senha', 'password2': 'Confirmação de Senha', 'tipo_usuario': 'Tipo de Usuário', 'telefone': 'Telefone', 
            }

        # Vamos remover o tipo de usuário 'Administrador' da escolha # MODERADOR
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['tipo_usuario'].choices = [
            ('doador', 'Doador'), 
            ('adotante', 'Adotante')
        ]
     
