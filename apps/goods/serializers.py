# _*_coding: utf-8_*_
from rest_framework import serializers
from django.db.models import Q

from .models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd


class CategorySerializer3(serializers.ModelSerializer):
    """
    商品类别序列化
    """

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class GoodsCategoryBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class AdGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ("id", "goods_front_image")


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = GoodsCategoryBrandSerializer(many=True)
    # “商品”类型的对象必须是JSON可序列化的，
    # 注意serializer中的字段无论是新增加的还是重写的，它的对象都必须是JSON可序列化的
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_seralizer = None
        ad_goods = IndexAd.objects.filter(category=obj.id)
        if ad_goods:
            goods_ins = ad_goods[0].goods
            # 若serialzier中传递进去的是一个queryset,则many为True；否则为false
            goods_seralizer = AdGoodsSerializer(goods_ins, many=False,
                                                context={'request': self.context['request']})
        return goods_seralizer.data

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True,
                                           context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
