from flask_restful import abort
import app_config
from dxcaptcha.CaptchaClient import CaptchaClient
import hashlib

# 载入验证码
if app_config.YZM == 'DX':
    captchaClient = CaptchaClient(app_config.DX_config['AppID'], app_config.DX_config['AppSecret'])
    captchaClient.setTimeOut(4)


def abort_msg(status, msg):
    abort(status, status=status, msg=msg)


def ret_data(data=None, status=200):
    if data is None:
        status = 204
    return {'status': status, 'data': data}


def check_yzm_token(token):
    if app_config.YZM != 'DX':
        return True
    response = captchaClient.checkToken("token:")
    if response['serverStatus'] == 'SERVER_SUCCESS':
        if response['result'] is False:
            return False
        else:
            return True
    else:
        return False


def get_pwd(sid, pwd):
    hl = hashlib.md5()
    s = "oj%d %s" % (sid, pwd)
    hl.update(s.encode(encoding='utf-8'))
    return hl.hexdigest()
