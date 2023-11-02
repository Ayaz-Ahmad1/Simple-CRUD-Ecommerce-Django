from django.urls import path
from accounts import views

urlpatterns = [
    path('login', views.user_login,name='user_login'),
    path('logout', views.user_loguot,name='user_logout'),
    path('register', views.user_register,name='user_register'),
    path('profile/', views.profile,name='profile'),

]