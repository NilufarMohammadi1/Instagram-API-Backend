from .views import FileUploadView, PostsCreateAndList, UpdatePost, PostsCommenters, PostsLikers
from django.urls import path
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('', PostsCreateAndList.as_view(), name='fileUpload'),
    path('upload-file/', FileUploadView.as_view(), name='fileUpload'),
    path('<str:pk>/', UpdatePost.as_view(), name='UpdatePostList'),
    path('<str:pk>/comments', PostsCommenters.as_view(), name='PostsCommenters'),
    path('<str:pk>/likes', PostsLikers.as_view(), name='PostsLikers'),

]