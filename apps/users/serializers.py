# _*_coding: utf-8_*_

import re

from datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model

from SuperMarket.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_empty_values(self, data):
        """

        :param data:
        :return:
        """

    def validate_mobile(self, mobile):
        """
        实际上是def validate_empty_values(self, data)，
        必须改为函数名称必须为validate_ + 字段名
        验证手机号码
        :param data:
        :return:
        """

        # 手机号形式是否正确
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 手机是否注册
        if User.object.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # 添加时间大于一分钟以前。也就是距离现在还不足一分钟
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile):
            raise ValueError("距离上次发送不到１分钟")

        # 如果所有验证通过一定要把data，即moblie return回去
        return mobile
