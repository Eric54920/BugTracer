local_settings.py

```python
LANGUAGE_CODE = 'zh-hans'

# 腾讯云短信应用的 app_id
TENCENT_SMS_APP_ID = 1234567890

# 腾讯云短信应用的 app_key
TENCENT_SMS_APP_KEY = "xxx"

# 腾讯云短信签名内容
TENCENT_SMS_SIGN = "xxx"

TENCENT_SMS_TEMPLATE = {
    'register': xxxxxx,
    'login': xxxxxx,
    'resetpwd': xxxxxx
}
# 腾讯云存储appID
TENCENT_COS_APPID = xxxxxxxx
# 腾讯云存储ID
TENCENT_COS_ID = "xxxxxxx"
# 腾讯云存储KEY
TENCENT_COS_KEY = "xxxxxxxx"
# 腾讯云存储桶所在区域
TENCENT_COS_REGION = "ap-beijing"

# 数据库配置
DATABASES = {
    .....
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379", # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "" # redis密码
        }
    }
}

# 支付宝配置
ALIPAY = {
    .....
}
```