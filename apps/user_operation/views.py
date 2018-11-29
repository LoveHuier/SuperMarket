from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav
from .serializers import UserFavSerializer, UserFavDetailSerializer
from utils.permissions import IsOwnerOrReadOnly


# Create your views here.

class UserFavViewset(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    destroy:
        删除收藏
    """
    # 判断用户是否登录，是否有权限删除数据
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 若未登录，用jwt方式登录
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # serializer_class = UserFavSerializer
    lookup_field = "goods_id"

    # 重写get_queryset方法，获取当前user的userfavs，这样就只列出当前user的userfavs
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer

        return UserFavSerializer
