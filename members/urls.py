from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('profile/', views.user_profile, name='profile'),
    path('isuservalid/', views.is_user_valid, name='isuservalid'),
    path('isemailvalid/', views.is_email_valid, name='isemailvalid'),
    path('useractivation/', views.user_activation, name='userActivation'),
    path('mycart/', views.user_cart, name='cart'),
    path('cartoperation<str:type><int:id><str:action><int:doRedirect>/',
         views.cart_operation, name='cartoperation'),
]
