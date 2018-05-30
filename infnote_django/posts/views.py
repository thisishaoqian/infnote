import bson

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import PostSerializer, ContentlessPostSerializer


class CreatePost(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def post(request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = Post.objects.create(request.user, **serializer.validated_data)
            result = PostSerializer(instance=post).data
            return Response(result)

        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class ListPost(GenericAPIView):
    queryset = Post.objects.order_by('-date_submitted')
    serializer_class = ContentlessPostSerializer

    # TODO: 在查询数据库时排除 content 字段，以提高查询效率，减少发送的数据量
    # TODO: 需要增加 post 下的回复数量，浏览数量
    def get(self, request):
        queryset = self.get_queryset()
        category = request.query_params.get('category')

        # djongo 的 MongoDB ORM 不能连用 filter
        # 第一个后续的 filter 都会无效
        if category and len(category) > 0:
            queryset = queryset.filter(reply_to=None, category=category)
        else:
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
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ListReply(GenericAPIView):
    queryset = Post.objects.order_by('-date_submitted')
    serializer_class = PostSerializer

    def get(self, _, **kwargs):
        post_id = kwargs.get('id')
        post = self.get_queryset().get(id=bson.ObjectId(post_id))
        queryset = self.get_queryset().filter(reply_to=post.transaction_id)

        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
