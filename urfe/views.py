# urfe/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required  # Додано імпорт
from django.contrib.auth.models import User
from .models import Category, Material, UserProfile
from .forms import CustomUserCreationForm, CustomAuthenticationForm, MaterialForm, UserProfileForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def create_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)  # Обробка файлів
        if form.is_valid():
            material = form.save(commit=False)
            material.author = request.user
            material.save()
            messages.success(request, "Матеріал успішно створено!")
            return redirect('home')
        else:
            # помилки для діагностики
            print(form.errors)
    else:
        form = MaterialForm()
    return render(request, 'urfe/create_material.html', {'form': form})

@login_required
def home(request):
    materials = Material.objects.all().order_by('-created_at')
    
    # Фільтри та пошук
    category = request.GET.get('category')
    author_id = request.GET.get('author')
    search_query = request.GET.get('search', '')
    
    if category:
        materials = materials.filter(category__name=category)
    if author_id:
        materials = materials.filter(author_id=author_id)
    if search_query:
        materials = materials.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # Пагінація після фільтрації
    paginator = Paginator(materials, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.values_list('name', flat=True).distinct()
    authors = User.objects.prefetch_related('material_set').filter(material__isnull=False).distinct()
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    return render(request, 'urfe/home.html', {
        'page_obj': page_obj,  # Використовуємо page_obj замість materials
        'categories': categories,
        'authors': authors,
        'user_materials': Material.objects.filter(author=request.user),
        'favorite_materials': user_profile.favorite_materials.all(),
        'user_profile': user_profile,
    })

def material_detail(request, material_id):
    material = get_object_or_404(Material, pk=material_id)
    user_profile = UserProfile.objects.get(user=request.user)
    favorite_materials = user_profile.favorite_materials.all()
    return render(request, 'urfe/material_detail.html', {
        'material': material,
        'favorite_materials': favorite_materials
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'urfe/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                if user.userprofile.role == role:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Роль не відповідає.')
            except UserProfile.DoesNotExist:
                messages.error(request, 'Профіль не знайдено.')
        else:
            messages.error(request, 'Невірне ім’я або пароль.')
    
    return render(request, 'urfe/login.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('welcome')

def welcome(request):
    return render(request, 'urfe/welcome.html')

@login_required
def toggle_favorite(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)  # Захист від відсутнього профілю
    
    if material in user_profile.favorite_materials.all():
        user_profile.favorite_materials.remove(material)
    else:
        user_profile.favorite_materials.add(material)
    
    return redirect('home')

@login_required
def profile(request):
    user_profile = UserProfile.objects.select_related('user').get(user=request.user)
    user_materials = Material.objects.filter(author=request.user).select_related('category')
    
    return render(request, 'urfe/profile.html', {
        'user_profile': user_profile,
        'user_materials': user_materials,
    })

@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        if avatar:
            user_profile.avatar = avatar
            user_profile.save()
        return redirect('profile')
    return render(request, 'urfe/edit_profile.html', {'user_profile': user_profile})

@login_required
def edit_material(request, material_id):
    material = get_object_or_404(Material, id=material_id, author=request.user)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, 'Матеріал успішно оновлено!')
            return redirect('home')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'urfe/edit_material.html', {'form': form, 'material': material})

@login_required
def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id, author=request.user)
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Матеріал успішно видалено!')
        return redirect('home')
    return render(request, 'urfe/confirm_delete.html', {'material': material})