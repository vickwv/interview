import logging

from django.contrib.auth import get_user_model
from rest_framework import status

from api.abstract_views import AllowAnyView, NeedLoginView
from api.authentication import JWTAuthentication
from api.serializer import UserReqSerializer
from interview import settings

User = get_user_model()
log = logging.getLogger()


class UserSignUpView(AllowAnyView):
    serializer_class = UserReqSerializer

    def post(self, request):
        log.info("注册参数", extra=request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 创建用户账户
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        exist_user = User.objects.filter(email=email).first()
        if exist_user is not None:
            return AllowAnyView.fail(error_messages="请不要重复注册")
        try:
            user = User.objects.create_user(email=email, password=password)

            access_token = JWTAuthentication.create_jwt(user, "access", 24 * 30)
            refresh_token = JWTAuthentication.create_jwt(user, "access", 24 * 31)

            return AllowAnyView.success(data={'access_token': access_token,
                                              'refresh_token': refresh_token,
                                              'id': user.id,
                                              'email': user.email
                                              })
        except Exception as e:
            log.error("注册失败", extra=e.__dict__)
            return AllowAnyView.fail(error_messages="注册失败")


class UserSignInView(AllowAnyView):
    serializer_class = UserReqSerializer

    def post(self, request):
        log.info("登录参数", extra=request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            return AllowAnyView.fail("密码错误", status.HTTP_401_UNAUTHORIZED)

        access_token = JWTAuthentication.create_jwt(user, "access", settings.JWT_CONFIG['JWT_EXP'])
        refresh_token = JWTAuthentication.create_jwt(user, "access", settings.JWT_CONFIG['JWT_REF_EXP'])

        return AllowAnyView.success(data={'access_token': access_token,
                                          'refresh_token': refresh_token})


class UserInfoView(NeedLoginView):

    def get(self, request):
        user = request.user

        return AllowAnyView.success(data={'id': user.id, 'email': user.email})
