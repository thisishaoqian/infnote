from rest_framework.views import APIView
from rest_framework.response import Response
from utils.management.commands.migrateblocks import Command


class BlockUpdated(APIView):

    def get(self, request):
        Command.load_all()
        return Response('ok')
