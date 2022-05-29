import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager

# Create your models here.


class GameUsers(AbstractBaseUser,PermissionsMixin):
    id_user=models.CharField(max_length=7,primary_key=True)
    username=models.CharField('Introduzca su GamerTag',max_length=25, unique=True)
    password=models.CharField(max_length=25, unique=True)
    email=models.EmailField('Introduzca su Email',max_length=100, unique=True)
    img_perfil = models.ImageField(upload_to='users/', default='users/default.png')
    ganadas=models.PositiveIntegerField(default=0)
    perdidas=models.PositiveIntegerField(default=0)
    user_gamer=models.BooleanField(default=True)
    user_admin=models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['id_user','email','password']

    class Meta:
        verbose_name='Jugador'
        verbose_name_plural='Jugadores'

    @classmethod
    def create_gamer(cls,username,email,password):
        print(password)
        id_user = 'GT' + username[0] +str(random.randint(1000, 9999))
        user = cls(id_user=id_user,username=username,password=password,email=email)
        user.save()
        return user