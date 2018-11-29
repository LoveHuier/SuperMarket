# _*_coding: utf-8_*_

import re
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.models import Goods
from SuperMarket.settings import REGEX_MOBILE


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


class LeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言序列化类
    """
    # 获取当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'message_type', 'subject', 'message', 'file', 'id', 'add_time')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    signer_mobile = serializers.CharField(required=True, min_length=11, max_length=11,
                                          error_messages={
                                              "required": "签收电话不能为空",
                                              "min_length": "号码长度不对",
                                              "max_length": "号码长度不对"
                                          }, help_text='签收电话')

    def validate_signer_mobile(self, signer_mobile):
        # 手机号形式是否正确
        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError("手机号码非法")
        return signer_mobile

    province = serializers.CharField(required=True, error_messages={"required": "不能为空！"}, help_text='省份')
    city = serializers.CharField(required=True, error_messages={"required": "不能为空！"}, help_text='城市')
    district = serializers.CharField(required=True, error_messages={"required": "不能为空！"}, help_text='区域')
    address = serializers.CharField(required=True, error_messages={"required": "不能为空！"}, help_text='地址')
    signer_name = serializers.CharField(required=True, error_messages={"required": "不能为空！"}, help_text='签收人')

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address",
                  "signer_name", "add_time", "signer_mobile")
