from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name="home"),
    path('profile/<int:pk>/', profile, name="profile"),
    path('login/', loginPage, name="login"),
    path('register/', registerPage, name="register"),
]
