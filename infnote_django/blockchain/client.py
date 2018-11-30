import grpc
import json

from django.conf import settings
from users.serializers import UserBlockchainSerializer
from posts.serializers import PostBlockchainSerializer
from utils.singleton import Singleton

from .codegen.manage_server_pb2 import Payload
from .codegen.manage_server_pb2_grpc import BlockchainStub


class Client(metaclass=Singleton):
    def __init__(self):
        self.post_chain = settings.POST_CHAIN_ID
        self.user_chain = settings.USER_CHAIN_ID

    def create_post(self, post, public_key):
        post['id'] = post.pop('payload_id')
        self.create(self.post_chain, public_key, post, PostBlockchainSerializer)

    def create_user(self, user):
        public_key = user.pop('public_key')
        self.create(self.user_chain, public_key, user, UserBlockchainSerializer)

    @staticmethod
    def create(chain_id, public_key, data, serializer) -> str:
        with grpc.insecure_channel('localhost:32700') as channel:
            stub = BlockchainStub(channel)
            signature = data.pop('signature')
            content = json.JSONEncoder(ensure_ascii=False, separators=(',', ':')).encode(data).encode('utf8')
            response = stub.create_block(Payload(
                chain_id=chain_id,
                public_key=public_key,
                signature=signature,
                content=content
            ))
            if response.chain_id is not None and len(response.chain_id) > 0:
                data['block_time'] = response.time
                data['block_height'] = response.height
                s = serializer(data=data)
                if s.is_valid():
                    s.save()
                return response.chain_id
            elif response.chain_id == 'defered':
                return ''
            raise ValueError('Received a reponse without chain_id, there might be not the correct chain existed.')
