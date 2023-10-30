from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)

        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('非法登录')

        id = payload.get('user_identifier')
        if id is None:
            raise AuthenticationFailed('找不到用户')

        user = User.objects.filter(id=int(id)).first()
        if user is None:
            raise AuthenticationFailed('找不到用户')
        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user, token_type: str, hours: int):
        payload = {
            'user_identifier': user.id,
            'exp': int((datetime.now() + timedelta(hours=hours)).timestamp()),
            'iat': datetime.now().timestamp(),
            'token_type': token_type,
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')
        return token
