import datetime
import json
import os
import uuid

from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Users
from Comments.models import Comments
from Comments.serializers import CommentSerializer
from Likes.models import Likes
from Likes.serializers import LikeSerializer
from .models import Posts, Media
from .serializers import PostSerializer, MediaSerializer
import markdown
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from FinalDestination.settings import MARTOR_ENABLE_CONFIGS, MARTOR_MARKDOWN_BASE_MENTION_URL



class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MediaSerializer
    parser_classes = (MultiPartParser, FormParser,)
    ALLOWED_EXT = ["png", "jpg", "jpeg", "mp4", "mpeg", "mp3"]

    # queryset = FileSerializer.objects.all()
    def save_file(self, request, post_id):
        files = request.FILES.getlist('file')
        # print(request.data)
        saveFile = False
        for file in files:
            media_file_name = str(uuid.uuid4()) + file.name
            media_file_extension = media_file_name.split('.')[-1]
            if media_file_extension in self.ALLOWED_EXT:
                sub_directory = str(datetime.datetime.utcnow().strftime("%Y-%m-%d"))
                save_path = f'.\\media\\{sub_directory}\\'
                if not os.path.isdir(save_path):
                    os.makedirs(save_path)
                media_server_path = default_storage.save(f'{save_path}{media_file_name}', file)
                media_url = default_storage.url(media_server_path)
                content_type = file.content_type.lower()
                media_type = Media.MediaType.KNOWN
                if content_type.split('/')[0] == "image":
                    media_type = Media.MediaType.IMAGE
                if content_type.split('/')[0] == "video":
                    media_type = Media.MediaType.VIDEO
                serializer_data = {
                    "media_type": media_type,
                    "media_url": media_url,
                    "content_type": content_type,
                    "media_file_name": media_file_name,
                    "media_file_extension": media_file_extension,
                    "media_server_path": media_server_path,
                    "post": post_id
                }
                file_serializer = MediaSerializer(data=serializer_data)
                if file_serializer.is_valid():
                    file_serializer.save()
                    saveFile = True
        return saveFile

    def post(self, request, *args, **kwargs):
        post_id = request.data["post_id"]
        saveFile = self.save_file(request, post_id)

        if saveFile:
            return Response({'status': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': False}, status=status.HTTP_400_BAD_REQUEST)


class PostsCreateAndList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        data['post_owner'] = request.user.id
        data['hashtag'] = []
        post_serializer = PostSerializer(data=data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePost(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    multiple_lookup_fields = ['pk']

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class PostsCommenters(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.filter(post=self.kwargs.get("pk"))



class PostsLikers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer


    def get_queryset(self):
        return Likes.objects.filter(post=self.kwargs.get("pk"))



# class GetUserPosts(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer
#
#     def get_queryset(self):
#         print('userid-->', self.kwargs.get("pk"))
#         return Posts.objects.filter(post_owner=self.kwargs.get("pk"))