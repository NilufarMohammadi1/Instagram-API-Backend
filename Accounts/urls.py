from ratelimit.decorators import ratelimit

from .views import RegisterAPI, GetUserPosts, FollowAction, UserFollowers, UserFollowings
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import ChangePasswordView


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', ratelimit(key="ip", rate='1/min', block=True)(jwt_views.TokenObtainPairView.as_view())),
    path('refresh_token/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('<str:pk>/posts/', GetUserPosts.as_view(), name='GetUserPosts1'),
    path('posts/', GetUserPosts.as_view(), name='GetUserPosts'),

    path('follow/<str:dest_user>/', FollowAction.as_view(), name='UserFollowing'),


    path('followers/', UserFollowers.as_view(), name='Followers'),
    path('<str:pk>/followers/', UserFollowers.as_view(), name='UserFollowers'),

    path('followings/', UserFollowings.as_view(), name='Followings'),
    path('<str:pk>/followings/', UserFollowings.as_view(), name='UserFollowings'),
]