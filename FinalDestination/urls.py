
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views
from Accounts.views import ChangePasswordView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('Accounts.urls')),
    path('posts/', include('Posts.urls')),
    path('comment/', include('Comments.urls')),
    path('like/', include('Likes.urls')),
]
