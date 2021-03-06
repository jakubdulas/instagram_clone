from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_images/', default='profile_images/default-profile.jpg')
    bio = models.TextField(blank=True)
    following = models.ManyToManyField(User, related_name='following')
    followers = models.ManyToManyField(User, related_name='followers')

    def __str__(self):
        return self.user.username

    @property
    def total_following(self):
        return self.following.all().count()

    def profile_posts(self):
        return self.post_set.all()



class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, upload_to='images/')
    body = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likes')
    liked = models.BooleanField(null=True, blank=True, default=False)
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.author) + ' | '+ str(self.id)

    @property
    def total_likes(self):
        return self.likes.all().count()

    def post_comments(self):
        return self.comment_set.all()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    comment_body = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name="commentLikes")

    def __str__(self):
        return str(self.post.id) + ' | ' + str(self.post.author)

    @property
    def total_likes(self):
        return self.likes.all().count()

    

