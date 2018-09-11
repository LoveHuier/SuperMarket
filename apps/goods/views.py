from goods.serializers import GoodsSerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory
from .filters import GoodsFilter


# Create your views here.

class GoodsPagination(PageNumberPagination):
    # 每页显示多少个
    page_size = 10
    # 默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数
    page_size_query_param = "size"
    # 最大页数不超过10
    max_page_size = 50
    # 获取页码数的
    page_query_param = "page"


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表页，分页，搜索，过滤，排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('add_time', 'sold_num', 'fav_num')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer


class GoodsListView(generics.ListAPIView):
    """
    商品列表页
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    # def get(self, request, format=None):
    #     goods = Goods.objects.all()[:10]
    #     goods_serializer = GoodsSerializer(goods, many=True)
    #
    #     return Response(goods_serializer.data)
