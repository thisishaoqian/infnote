from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from blockchain import RPCClient

from .models import *
from .serializers import PostSerializer, PostBriefSerializer, ReplySerializer


class CreatePost(APIView):

    @staticmethod
    def post(request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=serializer.validated_data.get('user_id'))
            if user is not None:
                if RPCClient().create_post(serializer.validated_data, user.public_key) is not None:
                    serializer.save()
                return Response(serializer.validated_data)
            return Response({'user': 'The user id is not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListPost(GenericAPIView):
    queryset = Post.objects.order_by('-block_time').order_by('-date_submitted')
    serializer_class = PostBriefSerializer

    def get(self, request):
        queryset = self.get_queryset()
        confirmed = request.query_params.get('confirmed', None)
        user_id = request.query_params.get('user', None)
        safe = request.query_params.get('safe', True)

        # IMPORTANT: djongo has a query problem, reply_to just cannot put to front
        if confirmed is not None:
            queryset = queryset.filter(block_time__gt=0)

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)

        if bool(int(safe)):
            queryset = queryset.filter(nsfw=False)

        queryset = queryset.filter(reply_to=None)
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrievePost(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'payload_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ListReply(GenericAPIView):
    queryset = Post.objects.order_by('-date_submitted')
    serializer_class = ReplySerializer

    def get(self, _, **kwargs):
        post_id = kwargs.get('payload_id')
        post = self.get_queryset().get(payload_id=post_id)
        queryset = self.get_queryset().filter(reply_to=post.payload_id).order_by('date_submitted')

        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
