# _*_coding: utf-8_*_

import re

from datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from SuperMarket.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

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
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # 添加时间大于一分钟以前。也就是距离现在还不足一分钟
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile):
            raise ValueError("距离上次发送不到１分钟")

        # 如果所有验证通过一定要把data，即moblie return回去，因为数据要保存到db中
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    # 1.验证验证码是否合法
    code = serializers.CharField(required=True, write_only=True, max_length=6, min_length=6, error_messages={
        "blank": "请输入验证码",
        "required": "请输入验证码",
        "max_length": "验证码长度出错",
        "min_length": "验证码长度出错",
    }, label='验证码', help_text='验证码')

    # 验证username是否存在，是否唯一
    username = serializers.CharField(required=True, allow_blank=False, label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在")])
    password = serializers.CharField(required=True, style={
        "input_type": "password"
    }, label='密码', write_only=True)

    def validate_code(self, code):
        # 2.检查验证码是否存在，且按add_time倒序排．只验证最新的一条
        verify_codes = VerifyCode.objects.filter(mobile=self.initial_data['mobile']).order_by('-add_time')
        if verify_codes:
            last_code = verify_codes[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            # 3.检查验证码是否过期
            if five_minutes_ago > last_code.add_time:
                raise serializers.ValidationError("验证码过期")

            # 4.检查验证码的值是否正确
            if last_code.code != code:
                raise serializers.ValidationError("验证码错误")

                # return code可以return也可以不return，因为code只是用来做验证，不是需要保存到数据库中．
        else:
            # 验证码记录不存在
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        """
        不加字段名的验证器作用于所有字段之上．对验证后的字段进行统一的处理．
        :param attrs: 每个字段validate之后，总的字段的dict
        :return:
        """
        # attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'mobile', 'code', "password")
