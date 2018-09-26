from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import UserSerializer, NonceTokenSerializer


class CreateUser(APIView):
    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateInfo(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

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


class UserDetail(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        # Setting both '/user/' and '/user/<id>/' to this class
        # if lookup_url_kwarg not exist and authenticated, then return the current user object
        # otherwise return None
        if lookup_url_kwarg in self.kwargs:
            user_id = self.kwargs[lookup_url_kwarg]
        elif self.request.user:
            return self.request.user
        else:
            return None

        filter_kwargs = {self.lookup_field: user_id}
        obj = generics.get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class Token(APIView):

    @staticmethod
    def get(request):
        public_key = request.query_params.get('public_key', None)
        token = NonceToken.objects.create(public_key)
        serializer = NonceTokenSerializer(instance=token)

        return Response(serializer.data)
