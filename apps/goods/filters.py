# _*_coding: utf-8_*_

from django_filters import rest_framework as filters

from .models import Goods


class GoodsFilter(filters.FilterSet):
    """
    商品过滤类
    """
    min_price = filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')

    # name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Goods
        fields = ['min_price', 'max_price']
