from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'phone', 'password', 'is_active',
                  'first_name', 'last_name', 'bio', 'gender', 'website', 'birthday',
                  'avatar', 'is_private', 'date_joined', 'status']

        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        print('validated_data->>>>', validated_data)
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        user = super(UserSerializer, self).update(instance, validated_data)
        try:
            user.set_password(make_password(validated_data['password']))
            user.save()
        except Exception as ex:
            pass

        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = UserSerializer

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
#ali in fayde ndre ebayad kolesh pak sshe baz
# yekam sabr kon age nashodchasasssssssssssssssssssssssssh

# midoni chera chon masalan vaghti dari ro snapp develop mikoni nemitoni data snapp ro pak koni chon error mide
#ghashang budd

# class UserFollowSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Followings
#         fields = ["user_base", "user_dest"]
#
#         extra_kwargs = {
#             "user_base": {
#                 "read_only": True,
#             }
#         }

