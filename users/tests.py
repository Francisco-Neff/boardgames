import imp
from django.test import TestCase
from .models import GameUsers
# Create your tests here.

class GameUsersTest(TestCase):

    #Crear Jugador
    GameUsers(
        username='JugadorTest',
        password='LG4WFjihVhDWGyE',
        email='test@test.com'
    ).save()

