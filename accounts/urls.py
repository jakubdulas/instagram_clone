from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name="home"),
    path('profile/<int:pk>/', profile, name="profile"),
    path('register/', registerPage, name="register"),
    path('logout/', logoutUser, name="logout"),
]
