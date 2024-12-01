from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth import login, authenticate

from adote.models import Animal, Local, TipoAnimal, Usuario
from adote.forms import AnimalForm, RegistroForm

# Funções auxiliares
def is_admin(user):
    """
    Verifica se o usuário é um administrador.
    """
    return user.is_authenticated and user.is_admin()

# Páginas públicas
def pagina_inicial(request):
    """
    Renderiza a página inicial.
    """
    return render(request, 'pagina_inicial.html')

def registro(request):
    """
    Página de registro de novos usuários.
    """
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def detalhes_animal(request, animal_id):
    """
    Página de detalhes de um animal específico.
    """
    animal = get_object_or_404(Animal, id=animal_id)
    return render(request, 'detalhes_animal.html', {'animal': animal})

# Áreas protegidas
@login_required
def lista_animais(request):
    """
    Lista de todos os animais, com suporte a filtros por cidade, tipo e status de adoção.
    """
    animais = Animal.objects.all()
    locais = Local.objects.all()
    tipos = TipoAnimal.objects.all()

    # Filtros
    cidade = request.GET.get('cidade')
    if cidade:
        animais = animais.filter(local__cidade=cidade)

    adotado = request.GET.get('adotado')
    if adotado == 'adotados':
        animais = animais.filter(adotado=True)
    elif adotado == 'nao_adotados':
        animais = animais.filter(adotado=False)

    tipo_animal = request.GET.get('tipo')
    if tipo_animal:
        animais = animais.filter(tipo__nome=tipo_animal)

    context = {
        'animais': animais,
        'locais': locais,
        'tipos': tipos,
    }
    return render(request, 'lista_animais.html', context)

@login_required
def adotar_animal(request, animal_id):
    """
    Marca um animal como adotado, associando-o ao usuário atual (se for adotante).
    """
    if not request.user.is_adotante():
        return HttpResponseForbidden("Apenas adotantes podem acessar esta página.")

    animal = get_object_or_404(Animal, id=animal_id)
    animal.adotante = request.user
    animal.adotado = True
    animal.save()

    return render(request, 'adotar_animal.html', {'animal_id': animal_id})

@login_required
def doar_animal(request):
    """
    Página para doação de um novo animal, associando-o ao doador logado.
    """
    if not request.user.is_doador():
        return HttpResponseForbidden("Apenas doadores podem acessar esta página.")

    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.doador = request.user
            animal.save()
            return redirect('lista_animais')
    else:
        form = AnimalForm()

    return render(request, 'doar_animal.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def area_admin(request):
    """
    Área administrativa acessível apenas para administradores.
    """
    return render(request, 'admin_area.html')

@login_required
@user_passes_test(is_admin)
def marcar_adotado(request):
    """
    Permite a um administrador marcar um animal como adotado.
    """
    animais = Animal.objects.filter(adotado=False)  # Apenas animais não adotados
    if request.method == 'POST':
        animal_id = request.POST.get('animal_id')
        animal = get_object_or_404(Animal, id=animal_id)
        animal.adotado = True
        animal.save()
        return redirect('marcar_adotado')

    return render(request, 'marcar_adotado.html', {'animais': animais})

@login_required
@user_passes_test(is_admin)
def adicionar_pet(request):
    """
    Permite adicionar novos animais ao sistema.
    """
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('area_admin')
    else:
        form = AnimalForm()

    # Adicionando classe CSS para estilização
    for field in form:
        field.field.widget.attrs.update({'class': 'form-control'})

    return render(request, 'adicionar_pet.html', {'form': form})

# Páginas auxiliares
def deslogado(request):
    """
    Página exibida após o logout.
    """
    return render(request, 'logged_out.html')
