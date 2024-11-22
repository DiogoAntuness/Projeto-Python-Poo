from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from adote.models import Usuario 
from django.contrib.auth.decorators import login_required
from .models import Animal, Local
from .forms import AnimalForm
from django.http import HttpResponseForbidden
from .forms import UsuarioForm
from .forms import RegistroForm
from django.shortcuts import render

def pagina_inicial(request):
    return render(request, 'pagina_inicial.html')


# Página inicial - mostra uma lista de todos os animais
@login_required
def lista_animais(request):
    animais = Animal.objects.all()
    locais = Local.objects.all()

# Filtrando por cidade, se especificado na query
    cidade = request.GET.get('cidade')
    if cidade:
        animais = animais.filter(local__cidade=cidade)
    
    return render(request, 'lista_animais.html', {'animais': animais, 'locais': locais})

# Página de detalhes de um animal
@login_required
def detalhes_animal(request, animal_id):
    animal = Animal.objects.get(id=animal_id)
    return render(request, 'detalhes_animal.html', {'animal': animal})
# Registro de novo usuário
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

# Função para adotar um animal
@login_required
def adotar_animal(request, animal_id):
    if not request.user.is_adotante():
        return HttpResponseForbidden("Apenas adotantes podem acessar esta página.")
    animal = get_object_or_404(Animal, id=animal_id)
    animal.adotante = request.user
    animal.save()
    #return redirect('lista_animais')
    return render(request, 'adotar_animal.html', {'animal_id': animal_id})

#Funcao p/ doar um animal
@login_required
def doar_animal(request):
    if not request.user.is_doador():
        return HttpResponseForbidden("Apenas doadores podem acessar esta página.")
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.doador = request.user  # Associa o doador como o usuário logado
            animal.save()
            return redirect('lista_animais')
    else:
        form = AnimalForm()
    return render(request, 'doar_animal.html', {'form': form})
