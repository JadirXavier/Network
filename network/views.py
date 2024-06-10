from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.all().order_by('-timestamp')

    # Submit post
    if request.method == "POST":
        user = request.user
        body = request.POST["body"]
        created_post = Post(user=user, body=body)
        created_post.save()
        return redirect('index')

    return render(request, "network/index.html", {
        "posts": posts
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, username):
    posts = Post.objects.filter(user__username=username).order_by('-timestamp')
    user_profile = User.objects.get(username=username)
    user = request.user
    followers_count = Follow.objects.filter(followed=user_profile).count()
    following_count = Follow.objects.filter(follower=user_profile).count()
    follows = Follow.objects.filter(follower=user, followed=user_profile)
    return render(request, "network/profile.html", {
        "user_profile":user_profile,
        "posts":posts,
        "user":user,
        "follows":follows,
        "following_count":following_count,
        "followers_count":followers_count,
    })

@login_required
def follow(request, username):
    user_to_follow = User.objects.get(username=username)
    user_following = request.user

    if user_to_follow != user_following:
        Follow.objects.create(follower=user_following, followed=user_to_follow)

    return redirect('profile', username=username)

@login_required
def unfollow(request, username):
    user_to_follow = User.objects.get(username=username)
    user_following = request.user
    follow = Follow.objects.filter(follower=user_following, followed=user_to_follow)
    if user_to_follow != user_following:
        if follow.exists():
            follow.delete()

    return redirect('profile', username=username)