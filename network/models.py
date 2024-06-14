from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username} - {self.email}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def likes_count(self):
        return self.likes_received.count()

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp,
        }

    def __str__(self):
        return f"{self.user.username} posted at {self.timestamp}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_given")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes_received")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked at {self.timestamp}"

class Follow (models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} followed {self.follower}"