from django import forms

TTT_CHOICES = (
    ("X", "X Rayas"),
    ("O", "O Circulo"),
)

class BuscarSalaTTTForm(forms.Form):
    sala = forms.CharField(label='Introduzca el código de sala',max_length=5)
    ficha = forms.ChoiceField(choices = TTT_CHOICES)