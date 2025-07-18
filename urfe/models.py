# urfe/models.py
from django.db import models  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.core.validators import MaxLengthValidator

# Категорії матеріалів
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Навчальні матеріали
class Material(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    ROLE_CHOICES = (
        ('user', 'Студент'),
        ('teacher', 'Викладач'),
        ('admin', 'Адміністратор'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    favorite_materials = models.ManyToManyField(Material, blank=True, related_name='favorited_by')


    def __str__(self):
        return f"{self.user.username}'s Profile"