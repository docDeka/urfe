from django.contrib import admin
from .models import Category, Material, UserProfile, Zettel

admin.site.register(Category)
admin.site.register(Material)
admin.site.register(UserProfile)
admin.site.register(Zettel)
