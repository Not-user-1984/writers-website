from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.IndexHome.as_view(), name='index'),
    path('group/<str:slug>/', views.GroupPosts.as_view(), name='group_list'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('profile/<str:username>/', views.Profile.as_view(), name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path(
        'posts/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment',
    ),
    path('follow/', views.follow_index, name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow',
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow',
    )
]
