from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Like, Follow

# Index page
def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    user = request.user

    # Submit post
    if request.method == "POST":
        body = request.POST["body"]
        created_post = Post(user=user, body=body)
        created_post.save()
        return redirect('index')

    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for post in page_obj:
        # Creates a boolean key for each post object to follow if an user liked a post, and a title for the like_button tag 
        post.user_liked = post.likes_received.filter(user=user).exists()
        if post.user_liked == True:
            post.title = "Dislike"
        else:
            post.title = "Like"

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "current_user":user,
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

# Profile page
def profile(request, username):
    posts = Post.objects.filter(user__username=username).order_by('-timestamp')
    user_profile = User.objects.get(username=username)
    user = request.user
    followers_count = Follow.objects.filter(followed=user_profile).count()
    following_count = Follow.objects.filter(follower=user_profile).count()
    follows = None

    if user.is_authenticated:
        follows = Follow.objects.filter(follower=user, followed=user_profile)

    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for post in page_obj:
        # Creates a boolean key for each post object to follow if an user liked a post, and a title for the like_button tag 
        post.user_liked = post.likes_received.filter(user=user).exists()
        if post.user_liked == True:
            post.title = "Dislike"
        else:
            post.title = "Like"

    return render(request, "network/profile.html", {
        "user_profile":user_profile,
        "current_user":user,
        "follows":follows,
        "following_count":following_count,
        "followers_count":followers_count,
        "page_obj":page_obj
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

@login_required
def following(request):
    user = request.user
    follows = Follow.objects.filter(follower=user)
    followed_users = follows.values_list("followed__username", flat=True)
    posts = Post.objects.filter(user__username__in=followed_users).order_by('-timestamp')

    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for post in page_obj:
        # Creates a boolean key for each post object to follow if an user liked a post, and a title for the like_button tag 
        post.user_liked = post.likes_received.filter(user=user).exists()
        if post.user_liked == True:
            post.title = "Dislike"
        else:
            post.title = "Like"

    return render(request,"network/following.html", {
        "page_obj": page_obj,
        "current_user":user
    })

@login_required
def update_post(request, post_id):
    user = request.user
    try:
        post = Post.objects.get(user=user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            new_body = data.get("body")

            if not new_body:
                return JsonResponse({"error": "Body is required."}, status=400)
        
            post.body = new_body
            post.save()

            return JsonResponse({"success": "Post updated.", "post": post.serialize(user)})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
        
    else:
        return JsonResponse({"error": "PUT request required."}, status=405)
  
@login_required
def likes(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "POST":
        try:
            user = request.user
            existing_like = Like.objects.filter(user=user, post=post)

            if not existing_like:
                Like.objects.create(user=user, post=post)

            else:
                existing_like.delete()

            return JsonResponse({"post":post.serialize(user)})
        except:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
    else:
        return JsonResponse({"error": "POST request required."}, status=405)



