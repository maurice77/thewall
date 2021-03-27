
from django.urls import path
from . import views

urlpatterns = [
    path('', views.gotoLogin0),
    path('login', views.gotoLogin),
    path('success',views.showSuccess),
    path('login/signout',views.signOut),
    path('register',views.gotoRegister),
    path('register/checkEmail',views.checkEmail),
]