from flask_restful import Resource, reqparse, abort
from flask import session
from model import *
import app_config
import time
import base64
from tools import *
from app import app

# 代码自动保存

class AutoSave(Resource):
    def __init__(self):
        if 'uid' not in session:
            abort_msg(401, '未登录或登录过期!')

    def get(self, qid):
        # 从redis中取出
        r = app_config.save_redis
        uid = session.get('uid')
        try:
            data = r.get(f'{uid}_{qid}')
        except BaseException as e:
            abort_msg(500, '缓存连接失败!')
            app.logger.warning("Redis连接失败: %s" % str(e))
            return
        if data is None:
            abort_msg(404, '未保存或保存超时')
        return ret_data(data)

    def post(self, qid):
        parser = reqparse.RequestParser()
        parser.add_argument('code', type=str, required=True, nullable=False)
        args = parser.parse_args()
        uid = session.get('uid')
        try:
            coding_decrypt = base64.b64decode(args['code'].encode('utf-8')).decode()
        except BaseException as e:
            app.logger.warning("代码解码失败: %s" % (str(e)))
            abort_msg(500, 'BASE64解码失败')
            return
        if len(coding_decrypt) < 10:
            abort_msg(400, '代码过短不予保存')
        if len(coding_decrypt) > 20480:
            abort_msg(400, '欲保存的代码过长')
        r = app_config.save_redis
        try:
            r.setex(f'{uid}_{qid}', app_config.save_time, coding_decrypt)
        except BaseException as e:
            abort_msg(500, '缓存连接失败!')
            app.logger.warning("Redis连接失败: %s" % str(e))
            return
        return ret_data(None, 204)
