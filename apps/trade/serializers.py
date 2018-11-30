# _*_coding: utf-8_*_

from rest_framework import serializers

from .models import ShoppingCart
from goods.models import Goods


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label="数量", min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于一",
                                        "required": "请选择购买数量"
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        # 在view中直接从request中取出用户，但是在Serializer里不能直接从request中取，而是从context中取。
        user = self.context['request'].user
        existed = ShoppingCart.objects.filter(user=user, goods=validated_data['goods'])
        if existed:
            # 如果存在记录，则直接修改
            existed = existed[0]
            existed.nums += validated_data['nums']
            existed.save()

        else:
            # 因为结果要做反序列化交给前端的
            existed = ShoppingCart.objects.create(**validated_data)
        return existed
