import copy
import bson

from django.core.mail import send_mail

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import UserSerializer

from blockchain.core import Tool, Blockchain, b2lx, TX_FEE, SERVER_ADDRESS, script


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
            user = serializer.save()
            Tool.transfer_a_coin_to(user.public_address)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateInfo(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        # Try to get userinfo from tx
        if 'data' not in request.data:
            return Response({'data': 'Request JSON should have data field.'}, status=status.HTTP_400_BAD_REQUEST)
        raw_tx = request.data['data']
        blockchain = Blockchain()
        tx = blockchain.deserialize_transaction(raw_tx)

        # Find the transfer in tx
        addr = None
        vout = None
        data = None
        if len(tx.vout) > 1:
            d, flag = Blockchain.get_data_from_vout(tx.vout[0])
            if d and flag == script.OP_NOP8:
                vout = tx.vout[1]
            if vout.nValue >= TX_FEE * 2 and \
                    Blockchain.address_in_vout(vout) == SERVER_ADDRESS and \
                    flag == script.OP_NOP8:
                addr = Blockchain.address_in_vout(vout)
                vout = 1
                data = d

        if not addr or not vout:
            return Response(
                {'tx': 'You need transfer 2e5 with information to server at least.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate data and send transactions
        data['info_txid'] = b2lx(tx.GetTxid())
        data['is_confirmed'] = False
        serializer = UserSerializer(instance=request.user, data=data, partial=True)
        if serializer.is_valid():
            # Send userinfo tx
            blockchain.send_transaction(raw_tx)
            blockchain.freeze_coins_in_tx(tx)

            # Transfer the money (0) back to user means we verified the userinfo
            blockchain.send_raw_to(request.user.public_address, b2lx(tx.GetTxid()), vout, TX_FEE * 2)

            serializer.save()
            return Response(serializer.data)

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


class UserDetail(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

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
