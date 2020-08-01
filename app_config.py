import os
env_dist = os.environ
CLIENT_SECRET = "randstr"
WTF_CSRF_SECRET_KEY = CLIENT_SECRET
# 设置mysql的错误跟踪信息显示
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 打印每次模型操作对应的SQL语句
SQLALCHEMY_ECHO = True

SESSION_TYPE = "filesystem"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost:3306/APIOJ"

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_recycle': 120,
    'echo_pool': True,
    'pool_pre_ping': True,
    'pool_timeout': 5
}

YZM = None
DX_config = {
    'AppID': "ID",
    'AppSecret': "KEY"
}
gee_config = {
    'GEETEST_ID': "ID",
    'GEETEST_KEY': "KEY"
}
CSRF_Token = True
WTF_CSRF_TIME_LIMIT = 3600 * 6
