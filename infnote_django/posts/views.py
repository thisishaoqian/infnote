import bson

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
            RPCClient().create_post(serializer.save())
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListPost(GenericAPIView):
    queryset = Post.objects.order_by('-date_confirmed').order_by('-date_submitted')
    serializer_class = PostBriefSerializer

    def get(self, request):
        queryset = self.get_queryset()
        confirmed = request.query_params.get('confirmed', None)

        # IMPORTANT: djongo has a query problem, it cannot support chained filter calls
        params = {'reply_to': None}
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
    lookup_field = 'payload_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ListReply(GenericAPIView):
    queryset = Post.objects.order_by('-date_submitted')
    serializer_class = ReplySerializer

    def get(self, _, **kwargs):
        post_id = kwargs.get('id')
        post = self.get_queryset().get(id=bson.ObjectId(post_id))
        queryset = self.get_queryset().filter(reply_to=post.payload_id).order_by('date_submitted')

        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
