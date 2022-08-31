"""加密组件"""
from django.conf import settings
import hashlib


def md5(data):
    # 调用SECRET_KEY 为md5加入盐
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data.encode('utf-8'))
    return obj.hexdigest()

