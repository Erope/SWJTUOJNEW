from flask_restful import Resource, reqparse, abort
from flask import session
import app_config
from flask_wtf.csrf import CSRFProtect, generate_csrf
from tools import *
import json


class YZM(Resource):
    def get(self):
        if app_config.YZM == 'DX':
            return ret_data({'kind': 'DX', 'AppID': app_config.DX_config['AppID']})
        elif app_config.YZM == 'geetest':
            result = gee_register()
            session[GeetestLib.GEETEST_SERVER_STATUS_SESSION_KEY] = result.status
            r_data = json.loads(result.data)
            r_data['kind'] = 'geetest'
            return ret_data(r_data)
        else:
            abort_msg(404, '验证码未开启!')


class Token(Resource):
    def get(self):
        return ret_data({'token': generate_csrf()})
