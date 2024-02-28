from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_blog_categories,
         name='blogCategories'),
    path('blogDetails/', views.get_blog_details, name='blogDetails'),
    path('addComment/', views.add_comment, name='addComment'),
]
