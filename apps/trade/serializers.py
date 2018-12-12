# _*_coding: utf-8_*_
import time
from rest_framework import serializers

from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from utils.alipay import AliPay
from SuperMarket.settings import app_private_key_path, alipay_public_key_path


class GoodsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ("id", "name", "shop_price", "goods_front_image")


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsInfoSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = ("id", "goods", "nums")


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

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data['nums']
        instance.save()

        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsInfoSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        """
        生成支付的url
        :param obj:就是serializer对象
        :return:
        """
        alipay = AliPay(
            appid="2016092300577912",  # appid一定要改
            app_notify_url="http://112.74.176.52:8000/alipay/return/",
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,是否是debug模式
            return_url="http://112.74.176.52:8000/alipay/return/"  # 支付完成后要跳转到的目标url
        )
        url = alipay.direct_pay(
            # 因为订单里会有多个商品，所以标题改为我们自己商户的订单号。
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,  # 订单号每次要不一样
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 设置支付状态，订单号，交易号，支付时间为只读状态
    pay_status = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        """
        生成支付的url
        :param obj:就是serializer对象
        :return:
        """
        alipay = AliPay(
            appid="2016092300577912",  # appid一定要改
            app_notify_url="http://112.74.176.52:8000/alipay/return/",
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,是否是debug模式
            return_url="http://112.74.176.52:8000/alipay/return/"  # 支付完成后要跳转到的目标url
        )
        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,  # 订单号每次要不一样
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    def generate_order_sn(self):
        # 生成订单号，当前时间+userid+随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
