import json
import base58
import hashlib

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from blockchain.models import Block
from users.models import User
from users.serializers import UserImportSerializer
from posts.models import Post
from posts.serializers import PostImportSerializer


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.load_all()

    @staticmethod
    def load_all():
        for block in Block.objects.using('chains')\
                .filter(chain_id=settings.USER_CHAIN_ID, height__gt=0)\
                .order_by('height'):
            content = json.JSONDecoder().decode(block.payload.decode('utf8'))
            content['block_height'] = block.height
            content['block_time'] = block.time

            try:
                user = User.objects.get(id=content.get('id'))
            except ObjectDoesNotExist:
                user = None
            serializer = UserImportSerializer(user, data=content)
            if serializer.is_valid():
                serializer.save()
                print('User ID: "' + serializer.data.get('id') + '" saved.')
            else:
                print(serializer.errors)

        for block in Block.objects.using('chains')\
                .filter(chain_id=settings.POST_CHAIN_ID, height__gt=0)\
                .order_by('height'):
            content = json.JSONDecoder().decode(block.payload.decode('utf8'))
            content['block_height'] = block.height
            content['block_time'] = block.time

            serializer = PostImportSerializer(data=content)
            if serializer.is_valid():
                try:
                    serializer.save()
                    print(f'Saved: {content.get("id")}')
                except Exception:
                    print(f'Failed: {content.get("id")}')
            else:
                print(serializer.errors)

    @staticmethod
    def load_post(data):
        pass

    @staticmethod
    def load_user(data):
        pass
