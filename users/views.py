from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate ,login
from users.forms import RegistroUserForm, LoginGamerForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.

#Registro de un nuevo usuario
class Registro(View):
    template_name='registro.html'
    context={}
    form=RegistroUserForm()
    
    def get(self,request,*args,**kwargs):
        self.context['form']=self.form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=RegistroUserForm(request.POST)
        print(form.is_valid(),request.POST)
        if form.is_valid():
            form.save()
            ### TODO añadir el Login una vez registrado.
            return redirect('inicio')
        else:
            self.context['form']=self.form
            return render(request,self.template_name,self.context)

