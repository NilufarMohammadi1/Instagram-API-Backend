from django.urls import path
from .views import LikeList

urlpatterns = [
    path('<str:pk>/', LikeList.as_view(), name='LikeList')
]