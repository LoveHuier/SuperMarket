from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from SuperMarket.settings import APIKEY
from rest_framework.response import Response
from rest_framework import status
from random import choice
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from .models import VerifyCode

User = get_user_model()


# Create your views here.


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成六位数字的验证码
        """
        seeds = "1234567890"
        random_str = []
        for i in range(6):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        """
        重写CreateModelMixin中的create方法
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # 获取serializer验证mobile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 取出serializer验证通过后的数据validated_data中的mobile
        mobile = serializer.validated_data['mobile']

        # 发送验证码
        yun_pian = YunPian(APIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        # 判断发送成功与失败，以status的值为准，发送成功则保存到数据库
        if sms_status['code'] != 0:
            return Response({
                "mobile": sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 保存到数据库
            verify_code = VerifyCode(code=code, mobile=mobile)
            verify_code.save()

            return Response({
                'mobile': mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(UpdateModelMixin, CreateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """
    post:
        注册用户
    retrieve:
        用户详情
    """
    # serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 生成token
        user = self.perform_create(serializer)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # 存于serializer.data中
        re_dict = serializer.data
        re_dict['token'] = token
        # 像添加name一样，后期添加任何数据都可以，这样就可以将数据定制化
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        """
        动态设置serializer
        :return:
        """
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    def get_permissions(self):
        """
        动态设置权限
        :return:
        """
        if self.action == "retrieve":
            return [IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
