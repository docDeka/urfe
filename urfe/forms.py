from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Material, Category

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'description', 'category', 'file', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'role']
        widgets = {
            'role': forms.Select(attrs={'disabled': 'disabled'}),
        }
    
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'avatar')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                avatar=self.cleaned_data['avatar'],
                role=self.cleaned_data['role']
            )
        return user

class CustomAuthenticationForm(AuthenticationForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].widget.attrs.update({'class': 'form-control'})