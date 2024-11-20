from django.shortcuts import render
from .models import Animal, Local

# Página inicial - mostra uma lista de todos os animais
def lista_animais(request):
    animais = Animal.objects.all()
    locais = Local.objects.all()

# Filtrando por cidade, se especificado na query
    cidade = request.GET.get('cidade')
    if cidade:
        animais = animais.filter(local__cidade=cidade)
    
    return render(request, 'lista_animais.html', {'animais': animais, 'locais': locais})

# Página de detalhes de um animal
def detalhes_animal(request, animal_id):
    animal = Animal.objects.get(id=animal_id)
    return render(request, 'detalhes_animal.html', {'animal': animal})
