from django.shortcuts import render
from ratelimit.decorators import ratelimit
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Comments
from .serializers import CommentSerializer
from django.utils.decorators import method_decorator

# class CommentList(generics.ListCreateAPIView):
#     queryset = Comments.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def create_comment(self, serializer):
#         serializer.save(user_id=self.request.user)

#
# class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Comments.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]

class CommentList(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    @method_decorator(ratelimit(key='ip', rate='1/m',block=True))
    def post(self, request, *args, **kwargs):

        data = JSONParser().parse(request)
        data['user'] = request.user.id
        data['post'] = self.kwargs.get("pk")

        print('hiiii->', data)

        comment_serializer = CommentSerializer(data=data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
