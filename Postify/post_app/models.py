from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField("self", related_name="following", symmetrical=False, blank=True)
    # followers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    post_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    # dislike = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    comment_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.comment_user.user.username +' | '+self.post.title
    