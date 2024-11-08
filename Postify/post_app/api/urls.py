from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from post_app.api.views import (PostView, ProfileListView, ProfileView, PostCreate, 
                                CommentDetail, CommentView, ProfileCreate, PostDetail,
                                PostComments, CommentCreate, LikePost, FollowProfile,
                                LogOut_view, FollowingFollowers)

urlpatterns = [
    path('posts/', PostView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('posts/<int:pk>/comments/', PostComments.as_view(), name='post-comments'),
    path('posts/<int:pk>/comments/<int:c_pk>/', CommentDetail.as_view(), name='comments-detail'),
    path('posts/create/', PostCreate.as_view(), name='post-create'),
    path('posts/<int:pk>/like/', LikePost.as_view(), name='post-like'),
    path('profile/', ProfileListView.as_view(), name='user-list'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='user-detail'),
    path('profile/<int:pk>/followers/', FollowingFollowers.as_view(), name='following-followers'),
    path('profile/<int:pk>/follow/', FollowProfile.as_view(), name='profile-follow'),
    path('profile/create/', ProfileCreate.as_view(), name='profile-create'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogOut_view.as_view(), name='logout')
    # path('comments/', CommentView.as_view(), name='comments-list'),
    # path('comments/create/', CommentCreate.as_view(), name='comments-create'),
]