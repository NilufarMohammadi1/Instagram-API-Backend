import datetime
import json

from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from Posts.models import Posts
from Posts.serializers import PostSerializer
from .models import Users, Followings
from .permissions import FollowsUser
from .serializers import UserSerializer, UserSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import views as jwt_views
from ratelimit.decorators import ratelimit
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
#
# class CustomUserRateThrottle(AnonRateThrottle):
#     def parse_rate(self, rate):
#         return (3, 300)

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'



def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response



class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
            })
        else:
            return Response(user_serializer.errors)


def rate_limit(request, error):
    return JsonResponse({'status': 'Forbidden'})


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Users
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserPosts(generics.ListAPIView):
    permission_classes = [FollowsUser]
    serializer_class = PostSerializer

    def get_queryset(self):
        if "pk" in self.kwargs:
            selected_user = self.kwargs.get("pk")
        else:
            selected_user = self.request.user.id
        final_user = Users.objects.get(id=selected_user)
        # try:
        #     accepted_follower = Followings.objects.get(user_dest=final_user, user_base=self.request.user.id,
        #                                                pending=False)
        #     print('follower', accepted_follower)
        # except Exception as ex:
        #     accepted_follower = None
        #     print(ex)
        #

        # if final_user.is_private and final_user.id != self.request.user.id and not accepted_follower:
        #     return []

            # raise Http404("You are not allowed to access this user's posts")
            # return Response({'error':'User has a private account'}, 500)

        return Posts.objects.filter(post_owner=final_user)


class FollowAction(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    # serializer_class = UserFollowSerializer

    def post(self, request, *args, **kwargs):
        data = {}
        user_base = Users.objects.get(pk=request.user.id)
        try:
            user_dest = Users.objects.get(pk=self.kwargs.get("dest_user"))
        except Users.DoesNotExist:
            user_dest = None
            return Response({'status': 'User with this ID does not exist!'}, 500)

        if user_base == user_dest:
            return Response({'status': 'source and destination are the same!'}, 500)

        follow_object, created = Followings.objects.get_or_create(user_base=user_base, user_dest=user_dest)

        action = 'send_follow'
        if not created:
            action = 'remove_follow'
            follow_object.delete()
        else:
            follow_object.pending = user_dest.is_private
            if not user_dest.is_private:
                follow_object.accept_date = datetime.datetime.now()

            follow_object.save()

        return Response({'status': 'ok', 'action': action}, 200)


class UserFollowings(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if "pk" in self.kwargs:
            base_user = self.kwargs.get("pk")
        else:
            base_user = request.user.id

        selected_user = Users.objects.get(id=base_user)
        if selected_user.is_private and selected_user.id != self.request.user.id:
            return Response({'error': 'User has a Private account'}, 500)

        followers = Followings.objects.filter(user_base=base_user).values('user_dest')
        users_list = []
        for follower_id in followers:
            user_id = follower_id['user_dest']
            user_object = Users.objects.get(pk=user_id)
            data = {
                'username': user_object.username,
                'bio': user_object.bio,
                'avatar': user_object.avatar
            }
            users_list.append(data)
        return Response({'followings': users_list})


class UserFollowers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if "pk" in self.kwargs:
            user_dest = self.kwargs.get("pk")
        else:
            user_dest = request.user.id

        selected_user = Users.objects.get(id=user_dest)
        if selected_user.is_private and selected_user.id != self.request.user.id:
            return Response({'error': 'User has a Private account'}, 500)

        followers = Followings.objects.filter(user_dest=user_dest).values('user_base')
        users_list = []

        for follower_id in followers:
            user_id = follower_id['user_base']
            user_object = Users.objects.get(pk=user_id)
            data = {
                'username': user_object.username,
                'bio': user_object.bio,
                'avatar': user_object.avatar
            }
            users_list.append(data)

        return Response({'followers': users_list})
