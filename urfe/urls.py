# urfe/urls.py
from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
	path('accounts/login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('welcome/', views.welcome, name='welcome'),
    path('material/<int:material_id>/', views.material_detail, name='material_detail'),
    path('toggle-favorite/<int:material_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create-material/', views.create_material, name='create_material'),
    path('edit-material/<int:material_id>/', views.edit_material, name='edit_material'),
    path('delete-material/<int:material_id>/', views.delete_material, name='delete_material'),
]