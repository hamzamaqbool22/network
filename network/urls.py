
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path('profile/<str:username>/', views.user_profile , name = 'user_profile'),
    path('like_toggle/', views.like_toggle, name='like_toggle'),
    path('follow_toggle/', views.follow_toggle, name='follow_toggle'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('following/', views.following_posts, name='following_posts'),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
