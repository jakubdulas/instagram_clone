from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name="home"),
    path('<int:pk>/', profile, name="profile"),
    path('register/', registerPage, name="register"),
    path('logout/', logoutUser, name="logout"),
    path('like/<int:pk>', likePost, name="likePost"),
]
