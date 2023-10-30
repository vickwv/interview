from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class AbstractView(APIView):
    renderer_classes = [JSONRenderer]

    @classmethod
    def success(cls, data: dict):
        return Response({"code": 200, "message": "ok", "status": "success", "data": data}, 200)

    @classmethod
    def fail(cls, error_messages: str, code=200001, http_code=200):
        return Response({"code": code, "message": error_messages, "status": "fail"}, http_code)


class AllowAnyView(AbstractView):
    permission_classes = [permissions.AllowAny]

# 需验证登录态
class NeedLoginView(AbstractView):
    permission_classes = [IsAuthenticated]
