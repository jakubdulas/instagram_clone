from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .decorators import *
from django.contrib.auth.models import User
from django.views.generic import CreateView
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        posts = []
        for u in profile.following.all():
            following_profile = Profile.objects.get(user=u)
            for p in following_profile.following_posts():
                posts.append(p)
        for p in profile.post_set.all():
            posts.append(p)

        context = {'profile': profile, 'posts': posts}
        return render(request, 'home.html', context)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

        return render(request, 'login.html')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(author=profile)
    context = {'profile': profile, 'posts': posts}

    return render(request, 'profile.html', context)


@unauthenticated_user
def registerPage(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'register.html', context)

def logoutUser(request):
	logout(request)
	return redirect('home')

@login_required(redirect_field_name='home')
def likePost(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        post.liked = False
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.liked = True

    print(post.liked)
    return redirect('home')

@login_required(redirect_field_name='home')
def add_post(request):
    form = AddPostForm()
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        profile = Profile.objects.get(user=request.user)
        form.instance.author = profile
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'add_post.html', context)

@login_required(redirect_field_name='home')
def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    profile = post.author
    if request.user == profile.user:
        post.delete()
    return redirect('home')


@login_required(redirect_field_name='home')
@is_user_author
def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    form = EditPostForm(instance=post)
    if request.method == 'POST':
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'edit_post.html', context)

    
