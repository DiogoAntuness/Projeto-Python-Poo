from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth import login, authenticate

from adote.models import Animal, Local, TipoAnimal, Usuario, InteresseAdocao
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

def detalhes_animal(request, animal_id): #ATZ 1.2
    """
    Página de detalhes de um animal específico.
    """
    animal = get_object_or_404(Animal, id=animal_id)
    # Verificar se o usuário é o doador do animal ou um administrador
    if request.user.is_authenticated and (request.user == animal.doador or request.user.is_admin):
        return redirect('gerenciar_adocao', animal_id=animal_id)
    
    return render(request, 'detalhes_animal.html', {'animal': animal})

# Áreas protegidas
@login_required
@user_passes_test(is_admin)
def lista_adocoes(request): #ATZ 1.2
    """
    Lista todas as adoções realizadas.
    """
    adocoes = Adocao.objects.all()
    return render(request, 'lista_adocoes.html', {'adocoes': adocoes})

@login_required #ATZ 1.1 & 1.2
def gerenciar_adocao(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)

    # Verificar se o usuário é o doador do animal ou um administrador
    if request.user != animal.doador and not request.user.is_admin:
        return HttpResponseForbidden("Você não tem permissão para gerenciar esta adoção.")

    # Listar interessados
    interessados = InteresseAdocao.objects.filter(animal=animal)

    if request.method == 'POST':
        if 'adotante_id' in request.POST:
            adotante_id = request.POST.get('adotante_id')
            adotante = get_object_or_404(Usuario, id=adotante_id)
            
            # Marcar o animal como adotado e associar ao adotante
            animal.adotado = True
            animal.adotante = adotante
            animal.save()
        
        elif 'remover_adocao' in request.POST:
            # Remover a adoção e voltar para disponível
            animal.adotado = False
            animal.adotante = None
            animal.save()

        return redirect('detalhes_animal', animal_id=animal_id)

    return render(request, 'gerenciar_adocao.html', {'animal': animal, 'interessados': interessados})

@login_required #ATK 1.1
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


@login_required #ATZ 1.1
def quero_adotar(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)

    if request.user.tipo_usuario == 'adotante':
        # Adicione o usuário à lista de interessados
        interesse, created = InteresseAdocao.objects.get_or_create(adotante=request.user, animal=animal)
        
        # Recuperar a lista de interessados para exibição
        interessados = InteresseAdocao.objects.filter(animal=animal)
        return render(request, 'quero_adotar.html', {'animal': animal, 'interessados': interessados})
    
    return redirect('detalhes_animal', animal_id=animal_id)


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
    animais = Animal.objects.all()
    return render(request, 'admin_area.html', {'animais': animais})

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
@user_passes_test(is_admin) #ATZ 1.1
def adicionar_pet(request):
    """
    Permite adicionar novos animais ao sistema, com o administrador informando o doador e o contato.
    """
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.doador = request.user  # O administrador é o doador
            animal.save()
            return redirect('area_admin')
    else:
        form = AnimalForm()

    # Adicionando classe CSS para estilização
    for field in form:
        field.field.widget.attrs.update({'class': 'form-control'})

    return render(request, 'adicionar_pet.html', {'form': form})

@login_required
@user_passes_test(is_admin) #ATZ 1.1 - NOVO
def remover_pet(request, animal_id):
    """
    Permite remover um animal, seja ele para adoção ou já adotado.
    """
    animal = get_object_or_404(Animal, id=animal_id)
    if request.method == 'POST':
        animal.delete()
        return redirect('area_admin')
    
    return render(request, 'remover_pet.html', {'animal': animal})

@login_required
@user_passes_test(is_admin) #ATZ 1.2
def remover_pet_list(request):
    """
    Lista todos os animais para possível remoção.
    """
    animais = Animal.objects.all()
    return render(request, 'remover_pet_list.html', {'animais': animais})

# Páginas auxiliares
def deslogado(request):
    """
    Página exibida após o logout.
    """
    return render(request, 'logged_out.html')
