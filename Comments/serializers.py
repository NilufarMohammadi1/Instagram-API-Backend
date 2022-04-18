from rest_framework import serializers
from .models import Comments
from Accounts.models import Users
from Posts.models import Posts


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200, required=False)


    class Meta:
        model = Comments
        fields = ['id', 'user','post', 'comment_body', 'username']

        extra_kwargs = {
            'post': {'write_only': True},
            'username' : {'read_only': True}
        }

    def create(self, validated_data):
        return super(CommentSerializer, self).create(validated_data)

    def to_representation(self, instance):
        instance.username = instance.user.username
        data = super(CommentSerializer, self).to_representation(instance)
        return data