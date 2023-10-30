import re

from rest_framework import serializers

from api.models import User


class UserReqSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=20, required=False)
    email = serializers.CharField(max_length=32, required=True)
    password = serializers.CharField(max_length=32, required=True)

    def validate(self, data):
        data = super().validate(data)
        return data

    def validate_email(self, value):
        if len(value) > 20:
            raise serializers.ValidationError("邮箱最多允许20个字")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', value):
            raise serializers.ValidationError("请输入有效的邮箱地址")
        return value

    def validate_password(self, value):
        # 定义密码格式的正则表达式
        if not re.match(r'^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[+\-.]).{10,}$', value):
            raise serializers.ValidationError("密码必须包含数字、大写字母、小写字母和+-.符号，至少8个字符")
        return value
