from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from pymysql import NULL
from .forms import BuscarSalaTTTForm
from .models import TicTacToe

# Create your views here.
class BuscarSala(View):
    template_name='sala.html'
    form=BuscarSalaTTTForm()
    sala_libre = False
    context={}

    def get(self,request,*args,**kwargs):
        self.context['form']=self.form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=BuscarSalaTTTForm(request.POST)
        if form.is_valid():
            # Se buscan que exista algún registro de la sala, 
            # Si existe se comprueba que se tenga hueco libre para la ficha seleccionada.
                # Ficha
                    # Si las partidas existentes ninguna es iniciada o con hueco libre se le informa al usuario
            # Si no se tiene registro se redirecciona a la partida.
            registros = TicTacToe.objects.filter(sala_cod=int(form.cleaned_data.get('sala')))
            if registros.exists():
                print('registros1')
                if form.cleaned_data.get('ficha') == 'X':
                    registros = TicTacToe.objects.filter(Q(sala_cod=int(form.cleaned_data.get('sala'))) & Q(resultado='I') & Q(jugador_X=request.user.id_user))
                else:
                    registros = TicTacToe.objects.filter(Q(sala_cod=int(form.cleaned_data.get('sala'))) & Q(resultado='I') & Q(jugador_O=request.user.id_user))
                print(registros)
                if registros.exists():
                    self.context={'form': BuscarSalaTTTForm(),'error':'La ficha seleccionada esta ocupada o esta sala no tiene un hueco libre'}
                    return render(request, self.template_name, self.context)
            print('redirect')
            self.context = {'sala':form.cleaned_data.get('sala'),'ficha':form.cleaned_data.get('ficha')}
            return redirect('/ttt/partida/%s?&ficha=%s' %(form.cleaned_data.get('sala'), form.cleaned_data.get('ficha')))
            
        else:
            self.context['form']=self.form
            return render(request, self.template_name, self.context)


def game(request,sala):  
    ficha = request.GET.get("ficha")
    if request.user.is_authenticated:
        context = {
            "ficha": ficha, 
            "sala": sala,
        }
        return render(request, "tictactoe.html", context)
    else:
        return redirect('login')