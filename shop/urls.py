from django.urls import path
from . import views

urlpatterns = [
    path('productCategories/', views.get_product_categories,
         name='productCategories'),
    path('productDetails/', views.get_product_details, name='productDetails'),
    path('addComment/', views.add_comment, name='addComment'),
]
