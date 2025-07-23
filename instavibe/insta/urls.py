from django.urls import path
from . import views
from .views import create_post,  create_highlight
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('post/create/', create_post, name='create_post'),
    path('reels/', views.reels_view, name='reels'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('follow/<str:username>/', views.follow_toggle, name='follow_toggle'),
    path('posts/', views.post_list_view, name='post_list'),
    path('story/<int:story_id>/', views.story_detail_view, name='story_detail'),
    path('add-story/', views.add_story, name='add_story'),
    path('search/', views.search_users, name='search_users'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('explore/', views.explore, name='explore'),
    path('messages/', views.inbox, name='inbox'),
    path('messages/<int:user_id>/', views.conversation, name='conversation'),
    path('messages/send/<int:user_id>/', views.send_message, name='send_message'),
    path('notifications/', views.notifications, name='notifications'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('create-highlight/', create_highlight, name='create_highlight'),
    path('highlight/<int:highlight_id>/', views.highlight_detail, name='highlight_detail'),







]
