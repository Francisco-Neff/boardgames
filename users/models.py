import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager


# Create your models here.


class GameUsers(AbstractBaseUser):
    def contador():
        count = GameUsers.objects.count()
        if count == None:
            return 1
        else:
            return count + 1

    id_user=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,serialize=True)
    username=models.CharField('Introduzca su GamerTag',max_length=25, unique=True)
    password=models.CharField(max_length=250, unique=True)
    email=models.EmailField('Introduzca su Email',max_length=100, unique=True)
    img_perfil = models.ImageField(upload_to='users/', default='users/default.png')
    ganadas=models.PositiveIntegerField(default=0)
    sala_predefinida=models.PositiveIntegerField(unique=True,editable=True,default=contador)
    user_gamer=models.BooleanField(default=True)
    user_admin=models.BooleanField(default=False)


    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['id_user','email','password']


    class Meta:
        verbose_name='Jugador'
        verbose_name_plural='Jugadores'

    

