from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_blog_categories,
         name='blogCategories'),
    path('blogDetails<int:id>/', views.get_blog_details, name='blogDetails'),
    path('showBlog<int:id>/', views.show_blog, name='showBlog'),
    path('addComment<int:userID><int:blogID>/', views.add_comment, name='addComment'),
]
