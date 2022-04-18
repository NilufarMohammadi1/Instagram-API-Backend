import datetime
import json
import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core import serializers as szl
from rest_framework import serializers

from Accounts.models import Users
from Comments.models import Comments
from Likes.models import Likes
from .models import Posts, Media, Tag
from rest_framework.serializers import FileField
import os
from .utils import extract_hashtags
from django.db.models import Count
from django.db.models import Count




class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media

        fields = ['id', 'post', 'media_type', 'media_url', 'media_server_path', 'media_file_name',
                  'media_file_extension', 'created_at', 'modified_at']

    def create(self, validated_data):

        return super(MediaSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        post = super(MediaSerializer, self).update(instance, validated_data)
        try:
            post.save()
        except Exception as ex:
            pass

        return post


class PostSerializer(serializers.ModelSerializer):
    media = serializers.ListField(read_only=True)
    mentions = serializers.ListField(read_only=True)
    owner = serializers.ReadOnlyField()
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Posts
        fields = ['id', 'caption', 'category', 'category', 'hashtag', 'post_owner', 'media', 'post_mentions',
                  'mentions', 'owner', 'like_count', 'comment_count']
        extra_kwargs = {
            'post_mentions': {'write_only': True},
            'post_owner': {'write_only': True},
        }

    def create(self, validated_data):
        new_post_object = super(PostSerializer, self).create(validated_data)

        post_caption = validated_data['caption']
        extracted_hashtags = extract_hashtags(post_caption)


        for hashtag in extracted_hashtags:
            selected_tag, is_created = Tag.objects.get_or_create(title=hashtag)
            new_post_object.hashtag.add(selected_tag)

        new_post_object.save()
        return new_post_object

    def update(self, instance, validated_data):
        post = super(PostSerializer, self).update(instance, validated_data)
        try:
            post.hashtag.clear()
            post_caption = validated_data['caption']
            extracted_hashtags = extract_hashtags(post_caption)

            for hashtag in extracted_hashtags:
                selected_tag, is_created = Tag.objects.get_or_create(title=hashtag)
                post.hashtag.add(selected_tag)

            post.save()

        except Exception as ex:
            pass

        return post

    def to_representation(self, instance):
        media_list = Media.objects.filter(post_id=instance.id) \
            .values('id', 'media_url', 'media_file_name', 'media_file_extension')

        instance.owner = {
            'id': instance.post_owner.id,
            'username': instance.post_owner.username,
            'avatar': instance.post_owner.avatar,

        }

        instance.like_count = Likes.objects.filter(post=instance.id).count()
        instance.comment_count = Comments.objects.filter(post=instance.id).count()
        instance.media = media_list
        instance.mentions = instance.post_mentions.all().values('id', 'username')
        data = super(PostSerializer, self).to_representation(instance)
        return data

# class FileSerializer(serializers.ModelSerializer):
#     file = serializers.ListField(child=
#                                  serializers.FileField(max_length=100000,
#                                                        allow_empty_file=False, use_url=False))
#     post_id = serializers.IntegerField(allow_null=False)
#
#     class Meta:
#         model = Media
#         fields = ['file', 'post_id']
#
#     def create(self, validated_data):
#         return super(FileSerializer, self).create(validated_data)
#         # files = validated_data.pop('file')
#         #
#         # post_id = validated_data.pop('post_id')
#         # selected_post = Posts.objects.get(pk=post_id)
#         #
#         #
#         #
#         # media_file = Media.objects.create(post=selected_post, media_type=media_type,
#         #                                   media_url=media_url, media_server_path=media_server_path,
#         #                                   media_file_name=media_file_name,
#         #                                   media_file_extension=media_file_extension
#         #                                   )
#
#         # return selected_post
#
#     # def create(self, validated_data):
#     #     return super(FileSerializer, self).create(validated_data)
#     #
#     #
#     # def update(self, instance, validated_data):
#     #     post = super(FileSerializer, self).update(instance, validated_data)
#     #     try:
#     #         post.save()
#     #     except Exception as ex:
#     #         pass
#     #
#     #     return post
#
