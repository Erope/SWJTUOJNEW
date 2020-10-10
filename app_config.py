import os
import redis
import logging
from logging.handlers import TimedRotatingFileHandler

env_dist = os.environ
CLIENT_SECRET = "randstr"
WTF_CSRF_SECRET_KEY = CLIENT_SECRET
# 设置mysql的错误跟踪信息显示
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 打印每次模型操作对应的SQL语句
SQLALCHEMY_ECHO = True

# session有效期为1个月
PERMANENT_SESSION_LIFETIME = 31 * 24 * 60 * 60
SESSION_TYPE = "redis"
r = redis.Redis(host='localhost', port=6379, db=0)
SESSION_REDIS = r
# 反向解析用户登录session的redis
utos = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
# 保存代码的redis
save_time = 2 * 24 * 60 * 60
save_redis = redis.Redis(host='localhost', port=6379, db=2, decode_responses=True)

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost:3306/APIOJ"
SQLALCHEMY_BINDS = {
    'qu':        'mysql+pymysql://root:password@localhost:3306/Question'
}

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
CSRF_Token = False
WTF_CSRF_TIME_LIMIT = 3600 * 6

Avatar_Folder = "/data/fandai/sites/oj.shinenet.cn/www/Avatar/"
# 日志
formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
handler = TimedRotatingFileHandler(
    "/tmp/flask.log", when="D", interval=1, backupCount=15,
    encoding="UTF-8", delay=False, utc=True)
handler.setFormatter(formatter)
page_size = 15

# 进入数据库时是按id进入并非是按字符串进入，所以顺序千万不可动，也不可以删除
# 务必使用Python3.7及以上版本
# 保持和判题端相同的配置
languageOptions = [
    {'value': 'cpp'},
    {'value': 'c'},
    {'value': 'java'},
    {'value': 'python'}
]
