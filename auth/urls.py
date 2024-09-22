from django.urls import path
from . import views


urlpatterns = [
    path('api/userregister/', views.UserRegister, name='UserRegister'),
    path('api/userlogin/', views.UserLogin, name='UserLogin'),
    path('api/userlogout/', views.UserLogout, name='UserLogout'),
   
]