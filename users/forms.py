from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import GameUsers



class RegistroUserForm(UserCreationForm):
    class Meta:
        model=GameUsers
        fields=['username','email','password1','password2']
    def check_password(self):
        form=self.cleaned_data
        if form['password1'] != form['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return form['password2']
        
class ModificarAvatar(forms.ModelForm):
    class Meta:
        model=GameUsers
        fields=['img_perfil']

class ModificarPerfil(forms.ModelForm):
    class Meta:
        model=GameUsers
        fields=['username','email']