from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Category
from .serializers import CategroySerializer


class Categories(APIView):

    @staticmethod
    def get(_):
        return Response(CategroySerializer(many=True, instance=Category.objects.all()).data)
