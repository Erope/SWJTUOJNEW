from flask_restful import abort
from flask import session
import app_config
from dxcaptcha.CaptchaClient import CaptchaClient
from geetestsdk.geetest_lib import GeetestLib
import hashlib

# 载入验证码
if app_config.YZM == 'DX':
    captchaClient = CaptchaClient(app_config.DX_config['AppID'], app_config.DX_config['AppSecret'])
    captchaClient.setTimeOut(4)
elif app_config.YZM == 'geetest':
    gt_lib = GeetestLib(app_config.gee_config['GEETEST_ID'], app_config.gee_config['GEETEST_KEY'])

def abort_msg(status, msg):
    abort(status, status=status, msg=msg)


def ret_data(data=None, status=200):
    if data is None:
        status = 204
    return {'status': status, 'data': data}


def check_yzm_token(token):
    if app_config.YZM != 'DX':
        return True
    response = captchaClient.checkToken(token)
    if response['serverStatus'] == 'SERVER_SUCCESS':
        if response['result'] is False:
            return False
        else:
            return True
    else:
        return False


def gee_register():
    digestmod = "md5"
    param_dict = {"digestmod": digestmod, "client_type": "web"}
    result = gt_lib.register(digestmod, param_dict)
    return result


def check_geetest(challenge, validate, seccode):
    status = session.get(GeetestLib.GEETEST_SERVER_STATUS_SESSION_KEY, None)
    # session必须取出值，若取不出值，直接当做异常退出
    if status is None:
        return False
    elif status == '1':
        param_dict = {"client_type": "web"}
        result = gt_lib.successValidate(challenge, validate, seccode, param_dict)
    else:
        result = gt_lib.failValidate(challenge, validate, seccode)
    # 注意，不要更改返回的结构和值类型
    if result.status == 1:
        return True
    else:
        return False


def get_pwd(sid, pwd):
    hl = hashlib.md5()
    s = "oj%d %s" % (sid, pwd)
    hl.update(s.encode(encoding='utf-8'))
    return hl.hexdigest()
