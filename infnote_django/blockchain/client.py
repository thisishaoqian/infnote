import grpc
import json

from datetime import datetime
from django.conf import settings
from posts.models import Post
from posts.serializers import PostBlockchainSerializer
from users.models import User
from users.serializers import UserBlockchainSerializer

from .codegen.manage_server_pb2 import Payload
from .codegen.manage_server_pb2_grpc import BlockchainStub


class Client:
    def __init__(self):
        self.post_chain = settings.POST_CHAIN_ID
        self.user_chain = settings.USER_CHAIN_ID

    def create_post(self, post: Post):
        self.create(self.post_chain, post, PostBlockchainSerializer)

    def create_user(self, user: User):
        self.create(self.user_chain, user, UserBlockchainSerializer)

    @staticmethod
    def create(chain_id, obj, serializer) -> str:
        with grpc.insecure_channel('localhost:32700') as channel:
            stub = BlockchainStub(channel)
            data = serializer(instance=obj).data
            string = json.JSONEncoder(ensure_ascii=False, separators=(',', ':')).encode(data)
            response = stub.create_block(Payload(chain_id=chain_id, content=string))
            if response.chain_id is not None and len(response.chain_id) > 0:
                obj.block_time = datetime.utcfromtimestamp(response.time)
                obj.block_height = response.height
                obj.save()
                return response.chain_id
            raise ValueError('Received a reponse without chain_id, there might be not the correct chain existed.')