from django.urls import path
from .views import CommentList

urlpatterns = [
    path('<str:pk>/', CommentList.as_view(), name='CommentList')
]