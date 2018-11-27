from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from blockchain import RPCClient

from .models import *
from .serializers import UserSerializer


class CreateUser(APIView):
    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if RPCClient().create_user(serializer.validated_data) is not None:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoID(APIView):
    @staticmethod
    def get(_, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data)


class UserInfoPK(APIView):
    @staticmethod
    def get(_, public_key):
        user = User.objects.get(public_key=public_key)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data)

