from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate ,login

from users.forms import RegistroUserForm, ModificarAvatar, ModificarPerfil
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GameUsers
from tictactoe.models import TicTacToe

# Create your views here.

#Registro de un nuevo usuario
class Registro(View):
    template_name='registro.html'
    context={'msg':'Registrate para poder jugar a nuestros juegos'}
    form=RegistroUserForm()
    
    def get(self,request,*args,**kwargs):
        self.context['form']=self.form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=RegistroUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password1'))
            if user is not None:
                login(request,user)
            return redirect('inicio')
        else:
            self.context['form']=self.form
            return render(request,self.template_name,self.context)


class Mostrarperfil(APIView):
    template_name='perfil.html'
    context = {}

    
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            ganadas,perdidas = TicTacToe.partidaslog(request.user.id_user)           
            self.context = {'ganadas':ganadas,'perdidas':perdidas,'avatarform':ModificarAvatar(),'modificarform':ModificarPerfil()}
            return render (request,self.template_name,self.context)
        else:
            return redirect('login')

    def post(self,request,*args,**kwargs):
        registro=GameUsers.objects.get(id_user=request.user.id_user)
        avatarform=ModificarAvatar(request.POST,request.FILES,instance=registro)
        if avatarform.is_valid():
            avatarform.save()
        return redirect('perfil')

    def put(self,request,*args,**kwargs):
        registro = GameUsers.objects.get(id_user=request.user.id_user)
        if registro.username != request.data['id_username'] or registro.email!= request.data['id_email']:
            GameUsers.objects.filter(id_user=request.user.id_user).update(username=request.data['id_username'],email=request.data['id_email'])
        return Response(status=status.HTTP_201_CREATED)

        
    


