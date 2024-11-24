from django.contrib import admin
from .models import Usuario, TipoAnimal, Local, Animal, Adocao, HistoriaAnimal

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin): #MODERADOR
   list_display = ('username', 'tipo_usuario', 'email', 'is_active')
   search_fields = ('username', 'email') 
   list_filter = ('tipo_usuario', 'is_active') 
   fields = ('username', 'email', 'tipo_usuario', 'telefone', 'is_active', 'is_staff', 'is_superuser') 
   readonly_fields = ('is_staff', 'is_superuser')

@admin.register(TipoAnimal)
class TipoAnimalAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('cidade', 'estado')
    search_fields = ('cidade', 'estado')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade_formatada', 'sexo', 'tipo', 'local', 'doador', 'adotado')
    search_fields = ('nome',)
    list_filter = ('tipo', 'local', 'adotado', 'sexo')

@admin.register(Adocao)
class AdocaoAdmin(admin.ModelAdmin):
    list_display = ('animal', 'adotante', 'data_adocao')
    search_fields = ('animal__nome', 'adotante__username')

@admin.register(HistoriaAnimal)
class HistoriaAnimalAdmin(admin.ModelAdmin):
    list_display = ('animal',)
    search_fields = ('animal__nome',)

