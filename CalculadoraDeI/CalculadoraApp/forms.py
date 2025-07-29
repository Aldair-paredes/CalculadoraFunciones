from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Perfil

class LoginForm(AuthenticationForm):
    pass

class RegistroForm(UserCreationForm):
    
    email = forms.EmailField(label="Correo electrónico", required=True)
    rol = forms.ChoiceField(choices=Perfil.ROLES, label="Rol")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) 

    def save(self, commit=True):
        user = super().save(commit=False)
        
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            rol = self.cleaned_data['rol']
            if not hasattr(user, 'perfil'):
                Perfil.objects.create(user=user, rol=rol)
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
