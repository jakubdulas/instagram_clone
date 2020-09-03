from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    #profile_pic = models.ImageField()
    bio = models.TextField(blank=True)
    #following = models.ManyToManyField(User, blank=True,  related_name='following')

    def __str__(self):
        return self.user.username

    @property
    def total_following(self):
        return self.following.all().count()

    def following_posts(self):
        return self.post_set.all()


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    body = models.TextField(null=True, blank=True)
    #likes = models.ManyToManyField(Profile, related_name='likes', null=True, blank=True)

    def __str__(self):
        return str(self.author)

