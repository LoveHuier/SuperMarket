from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .models import ShoppingCart
from .serializers import ShoppingCartSerializer, ShopCartDetailSerializer


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
