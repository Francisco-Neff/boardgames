from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('sala', login_required(views.BuscarSala.as_view()) ,name='sala' ),
    path('partida/<sala>', login_required(views.game) ),
]