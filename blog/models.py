from django.db import models
from members.models import Member
from django_resized import ResizedImageField

imagesDire = 'images/'
codesSourceDire = 'codeFiles/'
appsSourceDire = 'appFiles/'

# Create your models here.


class PostCategory(models.Model):
    title = models.CharField(null=False, max_length=50)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(null=False, max_length=50)
    contentText = models.TextField(blank=True)
    author = models.ForeignKey(
        Member, verbose_name='author', related_name='author', on_delete=models.CASCADE)
    category = models.ForeignKey(PostCategory, verbose_name="Category",
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Album(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    pic = ResizedImageField(
        size=[500, None], blank=True, null=True, upload_to=imagesDire)
    video = models.URLField(blank=True, null=True)
    category = models.ForeignKey(PostCategory, verbose_name="Category",
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    member = models.ForeignKey(
        Member, verbose_name='user', related_name='blog_commentator', on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    post = models.ForeignKey(
        Post, verbose_name='post', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    isActive = models.BooleanField(default=False)
