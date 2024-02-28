from django.shortcuts import render, redirect,reverse
from django.core import serializers
from django.http import JsonResponse
from .models import PostCategory, Post, Comment
from members.models import Member
import json


def get_blog_categories(request):
    response = dict()
    blogCats = PostCategory.objects.all()
    data = serializers.serialize('json', blogCats)
    response['cats'] = json.loads(data)
    return render(request, 'blog/blogCategories.html', response)
    # return JsonResponse(json.dumps(response), safe=False)


def get_blog_details(request, id):
    response = dict()
    blogs = Post.objects.filter(category=id)
    data = serializers.serialize('json', blogs)
    response['posts'] = json.loads(data)
    for post in range(len(response['posts'])):
        catID = response['posts'][post]['fields']['category']
        cat = PostCategory.objects.get(pk=catID)
        response['posts'][post]['fields']['category'] = cat
        authorID = response['posts'][post]['fields']['author']
        author = Member.objects.get(pk=authorID)
        response['posts'][post]['fields']['author'] = author
    return render(request, 'blog/blogDetails.html', response)
    # return JsonResponse(json.dumps(response), safe=False)


def show_blog(request, id):
    response = dict()
    blog = Post.objects.get(pk=id)
    # blog = serializers.serialize('json', blog)
    comments = Comment.objects.filter(post=id)
    comments = serializers.serialize('json', comments)
    response['blog'] = blog
    # response['blog'] = json.loads(blog)
    response['comments'] = json.loads(comments)
    return render(request, 'blog/blog.html', response)


def add_comment(request, userID, blogID):
    response = dict()
    commentText = request.POST['commentText']
    newComment = Comment.objects.create(
        member=Member.objects.get(pk=userID),
        post=Post.objects.get(pk=blogID),
        content=commentText,
    )
    newComment.save()
    response = redirect(reverse('blogCategories'))
    return response
