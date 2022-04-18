from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from Accounts.models import Users
from Posts.models import Posts
from .serializers import LikeSerializer
from Likes.models import Likes


class LikeList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # queryset = Likes.objects.all()
    # serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        data = {}
        #
        # data['user'] = request.user.id

        # data['post'] = kwargs.get("pk")
        # print('my post-->>>',data['post'])

        # mypost = Posts.objects.get(pk=self.kwargs.get("pk"))
        # inja baraye chi dobare neveshti ??
        # gerefti ? na ndidm dobar daram  migirm? are
        #  khob chikar kom

        # likes_serializer = LikeSerializer(data=data)
        # if likes_serializer.is_valid():
        #     likes_serializer.save()
        #     return Response(likes_serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(likes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        selected_post = None
        try: # my dg to variable ha bebinam jarime dare
             # kollan baaba khob dorosssh mikonm asan javab nmigrftm bara teste
             #  nemuudi maro ba jarime sotoon BIA benama :| in ebraze eshgh bud bishoor
            selected_post = Posts.objects.get(pk=self.kwargs.get("pk"))
        except Posts.DoesNotExist:
            return Response({'status': 'Post with this ID does not exist!'}, 500)

        liked_object, created = Likes.objects.get_or_create(post=selected_post, user=request.user)
        #
        action = 'like_post'
        if not created:
            action = 'remove_post_like'
            liked_object.delete()

            liked_object.save()

        return Response({'status': 'ok', 'action': action}, 200)


    #ay khoda huuuuuuuuuuuuf huuuuuuuuuuuuuuuuuuuuuuuuuf lov brm kelas majazai jbye