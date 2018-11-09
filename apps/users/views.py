from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from SuperMarket.settings import APIKEY
from rest_framework.response import Response
from rest_framework import status
from random import choice

from .serializers import SmsSerializer
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


class UserViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    注册用户
    """
    serializer_class = ''
