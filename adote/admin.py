from django.contrib import admin
from .models import Usuario, TipoAnimal, Local, Animal, Adocao, InteresseAdocao

admin.site.register(InteresseAdocao)#ATZ 1.1
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """
    Configurações do painel de administração para o modelo Usuario.
    """
    list_display = ('username', 'tipo_usuario', 'email', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('tipo_usuario', 'is_active')
    fields = ('username', 'email', 'tipo_usuario', 'telefone', 'is_active', 'is_staff', 'is_superuser')
    readonly_fields = ('is_staff', 'is_superuser')

@admin.register(TipoAnimal)
class TipoAnimalAdmin(admin.ModelAdmin):
    """
    Configurações do painel de administração para o modelo TipoAnimal.
    """
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    """
    Configurações do painel de administração para o modelo Local.
    """
    list_display = ('cidade', 'estado')
    search_fields = ('cidade', 'estado')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    """
    Configurações do painel de administração para o modelo Animal.
    """
    list_display = ('nome', 'idade_formatada', 'sexo', 'tipo', 'local', 'doador', 'adotado')
    search_fields = ('nome',)
    list_filter = ('tipo', 'local', 'adotado', 'sexo')
    fields = (
        'nome', 'idade_anos', 'idade_meses', 'sexo', 'tipo', 
        'local', 'descricao', 'foto', 'doador', 'adotante', 'adotado'
    )
    readonly_fields = ('adotante',)  # Impede edição direta do campo adotante no admin

@admin.register(Adocao)
class AdocaoAdmin(admin.ModelAdmin):
    """
    Configurações do painel de administração para o modelo Adocao.
    """
    list_display = ('animal', 'adotante', 'data_adocao')
    search_fields = ('animal__nome', 'adotante__username')
    list_filter = ('data_adocao',)

