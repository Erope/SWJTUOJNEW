from flask_restful import Resource, reqparse, abort
from flask import session
import app_config
from flask_wtf.csrf import CSRFProtect, generate_csrf
from tools import *


class YZM(Resource):
    def get(self):
        if app_config.YZM:
            return ret_data({'kind': 'DX', 'AppID': app_config.DX_config['AppID']})
        else:
            abort_msg(404, '验证码未开启!')


class Token(Resource):
    def get(self):
        return ret_data({'token': generate_csrf()})
