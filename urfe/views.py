# urfe/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Category, Material, UserProfile
from .forms import CustomUserCreationForm, CustomAuthenticationForm, MaterialForm, UserProfileForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def create_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.author = request.user
            material.save()
            messages.success(request, "Матеріал успішно створено!")
            return redirect('home')
        else:
            messages.error(request, "Помилка при створенні матеріалу. Перевірте форму.")
    else:
        form = MaterialForm()
    return render(request, 'urfe/create_material.html', {'form': form})

@login_required
def home(request):
    materials = Material.objects.all().order_by('-created_at')
    
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

    paginator = Paginator(materials, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.values_list('name', flat=True).distinct()
    authors = User.objects.prefetch_related('material_set').filter(material__isnull=False).distinct()
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    return render(request, 'urfe/home.html', {
        'page_obj': page_obj,
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

            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                'avatar': form.cleaned_data.get('avatar'),
                'role': form.cleaned_data.get('role')
                })

            login(request, user)
            messages.success(request, "Реєстрація успішна! Ласкаво просимо!")
            return redirect('home')
        else:
            messages.error(request, "Ой, схоже ви помилились, подивіться ще раз, дякую😉")
    else:
        form = CustomUserCreationForm()
    return render(request, 'urfe/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            role = form.cleaned_data.get('role')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                try:
                    profile = user.userprofile
                    if profile.role == role:
                        login(request, user)
                        messages.success(request, f"Вітаємо, {username}!")
                        return redirect('home')
                    else:
                        messages.error(request, "Обрана роль не відповідає вашому профілю")
                except UserProfile.DoesNotExist:
                    messages.error(request, "Профіль користувача не знайдено")
            else:
                messages.error(request, "Невірне ім'я користувача або пароль")
        else:
            messages.error(request, "Ой, схоже ви помилились, подивіться ще раз чи ви ввели правильні дані, дякую😉")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'urfe/login.html', {'form': form})

def welcome(request):
    return render(request, 'urfe/welcome.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Ви успішно вийшли з системи")
    return redirect('welcome')

@login_required
def toggle_favorite(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if material in user_profile.favorite_materials.all():
        user_profile.favorite_materials.remove(material)
    else:
        user_profile.favorite_materials.add(material)
    
    return redirect('home')

@login_required
def profile(request):
    return redirect('user_profile', user_id=request.user.id)

@login_required
def user_profile(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=target_user)
    user_materials = Material.objects.filter(author=target_user).select_related('category')
    
    is_own_profile = (request.user.id == user_id)

    return render(request, 'urfe/profile.html', {
        'user_profile': user_profile,
        'user_materials': user_materials,
        'is_own_profile': is_own_profile,
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
    return render(request, 'urfe/edit_material.html', {
    'form': form,
    'material': material,
    'object': material  # щоб шаблон не зламався, якщо десь використовується object
})

@login_required
def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id, author=request.user)
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Матеріал успішно видалено!')
        return redirect('home')
    return render(request, 'urfe/confirm_delete.html', {'material': material})

@login_required
def user_profile(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=target_user)
    user_materials = Material.objects.filter(author=target_user)

    return render(request, 'urfe/profile.html', {
        'user_profile': user_profile,
        'user_materials': user_materials,
    })
