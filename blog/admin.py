from django.contrib import admin
from .models import PostCategory, Post, Album, Comment

# Register your models here.
admin.site.register(PostCategory)
admin.site.register(Post)
admin.site.register(Album)
admin.site.register(Comment)
