from rest_framework import serializers
from .models import Likes
from Accounts.models import Users
from Posts.models import Posts


class LikeSerializer(serializers.ModelSerializer):
    user_like = serializers.CharField(max_length=200, required=False)
    class Meta:
        model = Likes
        fields = ['id', 'user','post','user_like']

    def create(self, validated_data):
        return super(LikeSerializer, self).create(validated_data)


    def to_representation(self, instance):
        user_like = instance.user.username
        instance.user_like = user_like
        data = super(LikeSerializer, self).to_representation(instance)
        return data