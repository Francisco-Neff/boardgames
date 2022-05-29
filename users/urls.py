from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from . import views

urlpatterns = [
    path('register/',views.Registro.as_view(),name='registro' ),
    path('login/',LoginView.as_view(template_name='registro.html'),name='login' ),
    path('logout/',LogoutView.as_view(),name='logout' ),
]