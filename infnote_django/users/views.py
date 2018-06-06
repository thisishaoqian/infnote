import copy
import bson

from django.core.mail import send_mail

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.permissions import IsOwnerOrReadOnly

from .models import *
from .serializers import UserSerializer


class CreateUser(APIView):
    @staticmethod
    def post(request):
        data = copy.deepcopy(request.data)
        # code = data.pop('vcode', None)
        # email = data.get('email')
        # if not VerificationCode.verify(email, code):
        #     return Response({'message': 'Verification code is invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Verification(APIView):
    @staticmethod
    def post(request):
        email = request.data.get('email')
        if not email:
            return Response({'message': 'email field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        vcode = VerificationCode.objects.create(email)
        result = send_mail(
            '[Infnote] Verification Code',
            'Your verification code is: ' + vcode.code,
            'donotreply@infnote.com',
            [email],
            fail_silently=False,
        )
        if result == 1:
            return Response({'message': 'Email has been sent.'})
        else:
            return Response({'message': 'Mail service failure.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class UserDetail(generics.RetrieveUpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly]

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

        filter_kwargs = {self.lookup_field: bson.ObjectId(user_id)}
        obj = generics.get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
