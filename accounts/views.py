from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .decorators import *
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        
        posts = []
        for u in profile.following.all():
            following_profile = Profile.objects.get(user=u)
            for p in following_profile.profile_posts():
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

@login_required(login_url='home')
def logoutUser(request):
	logout(request)
	return redirect('home')

@login_required(login_url='home')
def likePost(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        post.liked = False
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.liked = True
    return redirect('home')

@login_required(login_url='home')
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

@login_required(login_url='home')
def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    profile = post.author
    if request.user == profile.user:
        post.delete()
    return redirect('home')


@login_required(login_url='home')
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

@login_required(login_url='home')
def follow(request, pk):
    if request.method == 'POST':
        logged_profile = Profile.objects.get(user=request.user)
        profile_to_follow = Profile.objects.get(pk=pk)
        if logged_profile.following.filter(id=profile_to_follow.user.id).exists():
            logged_profile.following.remove(profile_to_follow.user)
            profile_to_follow.followers.remove(logged_profile.user)
        else:
            logged_profile.following.add(profile_to_follow.user)
            profile_to_follow.followers.add(logged_profile.user)
            
    return HttpResponseRedirect(reverse('profile', args=[str(profile_to_follow.user.username)]))

@login_required(login_url='home')
def add_comment(request, pk):
    form = AddCommentForm()
    post = Post.objects.get(pk=pk)
    author = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        form.instance.author = author
        form.instance.post = post
        if form.is_valid():
            form.save()
    return redirect('home')

@login_required(login_url='home')
def like_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('home')