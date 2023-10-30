import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.views import exception_handler

from api.abstract_views import AbstractView


def custom_exception_handler(exc, context):
    log = logging.getLogger()
    # 检查是否为参数验证异常
    if isinstance(exc, ValidationError):
        log.error("异常错误: ", extra=exc.detail)
        # 处理参数验证异常
        first_field, first_error = list(exc.detail.items())[0]
        return AbstractView.fail(error_messages=first_error)

    if isinstance(exc, NotAuthenticated):
        return AbstractView.fail(error_messages="未登录", http_code=status.HTTP_401_UNAUTHORIZED)

    response = exception_handler(exc, context)
    return response
