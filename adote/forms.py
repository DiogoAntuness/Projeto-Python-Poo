from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Animal, Usuario
# ------------------------------
# Formulários Relacionados a Animais
# ------------------------------
class AnimalForm(forms.ModelForm):
    """
    Formulário para adicionar ou editar um animal.
    Inclui validação personalizada para idade (anos ou meses).
    """
    class Meta:
        model = Animal
        fields = ['nome', 'idade_meses', 'idade_anos', 'sexo', 'tipo', 'local', 'descricao', 'foto']
        labels = {
            'nome': 'Nome do Animal',
            'idade_meses': 'Idade (em meses)',
            'idade_anos': 'Idade (em anos)',
            'sexo': 'Sexo',
            'tipo': 'Tipo de Animal',
            'local': 'Localização',
            'descricao': 'Descrição',
            'foto': 'Foto do Animal',
        }
    def clean(self):
        """
        Garante que apenas um dos campos de idade (anos ou meses) seja preenchido.
        """
        cleaned_data = super().clean()
        idade_anos = cleaned_data.get("idade_anos")
        idade_meses = cleaned_data.get("idade_meses")

        if idade_anos and idade_meses:
            raise forms.ValidationError("Preencha apenas um campo de idade: 'Idade (em anos)' ou 'Idade (em meses)'.")
        
        if not idade_anos and not idade_meses:
            raise forms.ValidationError("Informe a idade do animal, seja em anos ou meses.")
        
        return cleaned_data
# ------------------------------
# Formulários Relacionados a Usuários
# ------------------------------
class UsuarioForm(UserCreationForm):
    """
    Formulário para criação ou edição de usuários, incluindo campos adicionais.
    """
    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2', 'tipo_usuario', 'telefone']
        labels = {
            'username': 'Nome de Usuário',
            'password1': 'Senha',
            'password2': 'Confirmação de Senha',
            'tipo_usuario': 'Tipo de Usuário',
            'telefone': 'Telefone',
        }
class RegistroForm(UserCreationForm):
    """
    Formulário para registro de novos usuários. 
    Remove a opção de administrador para usuários comuns.
    """
    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2', 'tipo_usuario', 'telefone']
        labels = {
            'username': 'Nome de Usuário',
            'password1': 'Senha',
            'password2': 'Confirmação de Senha',
            'tipo_usuario': 'Tipo de Usuário',
            'telefone': 'Telefone',
        }
    def __init__(self, *args, **kwargs):
        """
        Remove a opção de 'Administrador' para usuários durante o registro.
        """
        super().__init__(*args, **kwargs)
        self.fields['tipo_usuario'].choices = [
            ('doador', 'Doador'),
            ('adotante', 'Adotante'),
        ]
