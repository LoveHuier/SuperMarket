from goods.serializers import GoodsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics

from .models import Goods


# Create your views here.

class GoodsListView(generics.ListAPIView):
    """
    商品列表页
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

        # def get(self, request, format=None):
        #     goods = Goods.objects.all()[:10]
        #     goods_serializer = GoodsSerializer(goods, many=True)
        #
        #     return Response(goods_serializer.data)
