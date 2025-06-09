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
    bio = models.TextField(
        max_length=100,
        validators=[MaxLengthValidator(100, message="Опис не може перевищувати 20 слів (100 символів).")],
        blank=True,
        help_text="Напишіть кілька слів про себе (до 20 слів)."
    )
    ROLE_CHOICES = (
        ('user', 'Користувач'),
        ('moderator', 'Модератор'),
        ('admin', 'Адміністратор'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    favorite_materials = models.ManyToManyField(Material, blank=True, related_name='favorited_by')


    def __str__(self):
        return f"{self.user.username}'s Profile"

# Zettel - короткі нотатки
class Zettel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    related = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.title