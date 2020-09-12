from django.shortcuts import redirect
from .models import *

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def is_user_author(view_func):
    def wrapper_func(request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        profile = post.author
        if request.user == profile.user:
            return view_func(request, pk, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper_func