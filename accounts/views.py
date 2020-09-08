from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from .decorators import *
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

def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    context = {'profile': profile}

    return render(request, 'profile.html', context)


@unauthenticated_user
def registerPage(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)

def logoutUser(request):
	logout(request)
	return redirect('home')

@login_required(redirect_field_name='home')
def likePost(request, pk):
    liked = False
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        liked = False
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True

    print(liked)
    return redirect('home')