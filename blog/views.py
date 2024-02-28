from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from .models import PostCategory, Post, Comment
from members.models import Member
import json


def get_blog_categories(request):
    response = dict()
    blogCats = PostCategory.objects.all()
    data = serializers.serialize('json', blogCats)
    response['cats'] = data
    return render(request,'blog/blogCategories.html', response)
    # return JsonResponse(json.dumps(response), safe=False)


def get_blog_details(request):
    response = dict()
    blogs = Post.objects.all()
    data = serializers.serialize('json', blogs)
    response['posts'] = json.loads(data)
    for post in range(len(response['posts'])):
        catID = response['posts'][post]['fields']['category']
        cat = PostCategory.objects.get(pk=catID)
        response['posts'][post]['fields']['category'] = cat
        authorID = response['posts'][post]['fields']['author']
        author = Member.objects.get(pk=authorID)
        response['posts'][post]['fields']['author'] = author
    return render(request,'blog/blogCategories.html', response)
    # return JsonResponse(json.dumps(response), safe=False)


def add_comment(request):
    response = dict()
    comments = Comment.objects.all()
    data = serializers.serialize('json', comments)
    response['comments'] = data
    return JsonResponse(json.dumps(response), safe=False)
