from goods.serializers import GoodsSerializer, CategorySerializer, BannerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory, Banner
from .filters import GoodsFilter


# Create your views here.

class GoodsPagination(PageNumberPagination):
    # 每页显示多少个
    page_size = 12
    # 默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数
    page_size_query_param = "size"
    # 最大页数不超过10
    max_page_size = 50
    # 获取页码数的
    page_query_param = "page"


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页，分页，搜索，过滤，排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('shop_price', 'sold_num')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
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


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图
    """
    serializer_class = BannerSerializer
    queryset = Banner.objects.all().order_by('index')
