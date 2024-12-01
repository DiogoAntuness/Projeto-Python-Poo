from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Constantes Globais
TIPOS_USUARIO = [
    ('doador', 'Doador'),
    ('adotante', 'Adotante'),
    ('admin', 'Administrador'),  # MODERADOR
]

SEXO_CHOICES = [
    ('M', 'Macho'),
    ('F', 'Fêmea'),
]

# Usuários
class Usuario(AbstractUser):
    """
    Modelo personalizado para representar usuários com diferentes papéis.
    """
    tipo_usuario = models.CharField(max_length=10, choices=TIPOS_USUARIO)
    telefone = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?\d{10,15}$',
            message="Telefone inválido. Use um número válido com 10 a 15 dígitos."
        )]
    )

    def is_doador(self):
        return self.tipo_usuario == 'doador'

    def is_adotante(self):
        return self.tipo_usuario == 'adotante'

    def is_admin(self):  # MODERADOR
        return self.tipo_usuario == 'admin'

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

# Animais e Tipos
class TipoAnimal(models.Model):
    """
    Modelo que define os tipos de animais (ex.: cães, gatos).
    """
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Tipo de Animal"
        verbose_name_plural = "Tipos de Animais"

class Local(models.Model):
    """
    Modelo que representa locais (cidade e estado).
    """
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cidade} - {self.estado}"

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"

class Animal(models.Model):
    """
    Modelo que representa animais disponíveis para adoção/doação.
    """
    nome = models.CharField(max_length=100)
    idade_anos = models.PositiveIntegerField(
        blank=True, null=True,
        help_text="Preencha apenas se a idade estiver em anos."
    )
    idade_meses = models.PositiveIntegerField(
        blank=True, null=True,
        help_text="Preencha apenas se a idade estiver em meses."
    )
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default='M')
    tipo = models.ForeignKey(TipoAnimal, on_delete=models.CASCADE, related_name="animais")
    descricao = models.TextField(blank=True)
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name="animais")
    adotado = models.BooleanField(default=False)
    adotante = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='animais_adotados'
    )
    doador = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='animais_doados'
    )
    foto = models.ImageField(upload_to='fotos_animais/', blank=True, null=True)

    def clean(self):
        """
        Validações personalizadas para a idade.
        """
        self.validate_idade()

    def validate_idade(self):
        if self.idade_anos and self.idade_meses:
            raise ValidationError('Preencha apenas um campo de idade: "idade_anos" ou "idade_meses".')
        if not self.idade_anos and not self.idade_meses:
            raise ValidationError('Informe a idade do animal, seja em anos ou meses.')

    @property
    def idade_formatada(self):
        """
        Retorna a idade formatada como anos ou meses.
        """
        if self.idade_anos:
            return f"{self.idade_anos} anos"
        elif self.idade_meses:
            return f"{self.idade_meses} meses"
        return "Idade não especificada"

    def __str__(self):
        return f"{self.nome} - {self.get_sexo_display()} ({self.idade_formatada})"

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animais"

# Adoções e Histórias
class Adocao(models.Model):
    """
    Modelo que registra adoções de animais.
    """
    animal = models.OneToOneField(Animal, on_delete=models.CASCADE, related_name="adocao")
    adotante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="adocoes")
    data_adocao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adotante.username} adotou {self.animal.nome}"

    class Meta:
        verbose_name = "Adoção"
        verbose_name_plural = "Adoções"

class HistoriaAnimal(models.Model):
    """
    Modelo que armazena as histórias de vida dos animais.
    """
    animal = models.OneToOneField(Animal, on_delete=models.CASCADE, related_name="historia")
    historia = models.TextField()

    def __str__(self):
        return f"História de {self.animal.nome}"

    class Meta:
        verbose_name = "História do Animal"
        verbose_name_plural = "Histórias dos Animais"
