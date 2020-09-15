from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name="home"),
    
    path('register/', registerPage, name="register"),
    path('logout/', logoutUser, name="logout"),
    path('like/<int:pk>', likePost, name="likePost"),
    path('add_post/', add_post, name='add_post'),
    path('delete_post/<int:pk>', delete_post, name='delete_post'),
    path('edit_post/<int:pk>', edit_post, name='edit_post'),
    path('follow/<int:pk>', follow, name='follow'),



    path('<str:username>/', profile, name="profile"),
]
