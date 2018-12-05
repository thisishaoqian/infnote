import json
import base58

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from blockchain.models import Block
from users.models import User
from users.serializers import UserImportSerializer
from posts.serializers import PostImportSerializer
from hooks.models import Migration


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.load_all()

    @staticmethod
    def load_all():
        try:
            user_chain_m = Migration.objects.get(chain_id=settings.USER_CHAIN_ID)
            user_height = user_chain_m.height
        except ObjectDoesNotExist:
            user_height = 0

        for block in Block.objects.using('chains')\
                .filter(chain_id=settings.USER_CHAIN_ID, height__gt=user_height)\
                .order_by('height'):
            content = json.JSONDecoder().decode(block.payload.decode('utf8'))
            content['block_height'] = block.height
            content['block_time'] = block.time
            user_height = block.height

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

        obj, _ = Migration.objects.get_or_create(chain_id=settings.USER_CHAIN_ID)
        obj.height = user_height
        obj.save()

        try:
            post_chain_m = Migration.objects.get(chain_id=settings.POST_CHAIN_ID)
            post_height = post_chain_m.height
        except ObjectDoesNotExist:
            post_height = 0

        for block in Block.objects.using('chains')\
                .filter(chain_id=settings.POST_CHAIN_ID, height__gt=post_height)\
                .order_by('height'):
            content = json.JSONDecoder().decode(base58.b58decode(block.payload).decode('utf8'))
            content['block_height'] = block.height
            content['block_time'] = block.time
            post_height = block.height

            serializer = PostImportSerializer(data=content)
            if serializer.is_valid():
                try:
                    serializer.save()
                    print(f'Saved: {content.get("id")}')
                except Exception:
                    print(f'Failed: {content.get("id")}')
            else:
                print(serializer.errors)

        obj, _ = Migration.objects.get_or_create(chain_id=settings.POST_CHAIN_ID)
        obj.height = post_height
        obj.save()

    @staticmethod
    def load_post(data):
        pass

    @staticmethod
    def load_user(data):
        pass
