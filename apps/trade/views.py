from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins

from utils.permissions import IsOwnerOrReadOnly
from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import ShoppingCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer


# Create your views here.


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能开发
    create:
        添加商品到购物车
    list:
        获取购物车详情
    create:
        加入购物车
    update:
        更新购物车中的订单
    delete:
        删除购物车中的订单
    """

    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShoppingCartSerializer
    lookup_field = "goods_id"

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer
        else:
            return ShoppingCartSerializer


class OrderViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create：
        新增订单
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # 获取到用户购物车里的商品
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)

        for shop_cart in shop_carts:
            # 将购物车中的商品添加到订单中
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            # 清空购物车数据
            shop_cart.delete()

        return order


from rest_framework.views import APIView
from utils.alipay import AliPay
from SuperMarket.settings import alipay_public_key_path, app_private_key_path


class AlipayView(APIView):
    def get(self, request):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """

    def post(self, request):
        """
        处理支付宝的notify_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for k, v in request.POST.items():
            processed_dict[k] = v
        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            appid="2016092300577912",  # appid一定要改
            app_notify_url="http://112.74.176.52:8000/alipay/return/",
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,是否是debug模式
            return_url="http://112.74.176.52:8000/alipay/return/"  # 支付完成后要跳转到的目标url
        )

        verify_re = alipay.verify(processed_dict, sign)
        print(verify_re)

