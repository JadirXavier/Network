
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile/<str:username>/follow/", views.follow, name="follow"),
    path("profile/<str:username>/unfollow/", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("post/<int:post_id>", views.update_post, name="update_post"),
    path("post/<int:post_id>/like", views.likes, name="likes"),

]
