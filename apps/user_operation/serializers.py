# _*_coding: utf-8_*_

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav
from goods.models import Goods


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='已经收藏'
            )
        ]
        fields = ("user", "goods", "id")


class UserFavGoodsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('name', "shop_price", 'id')


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = UserFavGoodsInfoSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")
