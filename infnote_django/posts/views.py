import bson

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import PostSerializer, PostBriefSerializer

from blockchain.core import Blockchain, b2lx


class CreatePost(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def post(request):
        if 'data' not in request.data:
            return Response({'data': 'Request JSON should have data field.'}, status=status.HTTP_400_BAD_REQUEST)
        raw_tx = request.data['data']
        blockchain = Blockchain()
        tx = blockchain.deserialize_transaction(raw_tx)
        data = blockchain.decode_transaction(tx)
        if len(data) > 0:
            data, _ = data[0]
        else:
            return Response({'tx': 'There is no data in it.'}, status=status.HTTP_400_BAD_REQUEST)

        data['transaction_id'] = b2lx(tx.GetTxid())
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            # TODO: 考虑是否将返回的内容计入余额或者是根据 block 来刷新
            # 先尝试发送 tx 如果有任何错误，就不会写入数据库了
            blockchain.send_transaction(raw_tx)
            blockchain.freeze_coins_in_tx(tx)

            post = Post.objects.create(request.user, **serializer.validated_data)

            result = PostSerializer(instance=post).data
            return Response(result)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListPost(GenericAPIView):
    queryset = Post.objects.order_by('-date_confirmed').order_by('-date_submitted')
    serializer_class = PostBriefSerializer

    # TODO: 在查询数据库时排除 content 字段，以提高查询效率，减少发送的数据量
    # TODO: 需要增加 post 下的回复数量，浏览数量
    def get(self, request):
        queryset = self.get_queryset()
        category = request.query_params.get('category')
        confirmed = request.query_params.get('confirmed', None)

        # djongo 的 MongoDB ORM 不能连用 filter
        # 第一个后续的 filter 都会无效
        params = {'reply_to': None}
        if category and len(category) > 0:
            params['category'] = category
        if confirmed is not None:
            params['is_confirmed'] = confirmed

        queryset = queryset.filter(**params)
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
        queryset = self.get_queryset().filter(reply_to=post.transaction_id).order_by('date_submitted')

        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
