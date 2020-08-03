from flask_restful import Resource, reqparse, abort
from flask import session
from model import *
import app_config
import time

from tools import *
from app import app


class Session(Resource):
    def post(self):
        # 检查用户当前登录状态
        if 'uid' in session:
            abort_msg(409, '您当前已经登录，不可重复登录!')
        # 检查post数据
        parser = reqparse.RequestParser()
        parser.add_argument('passwd', type=str, required=True, nullable=False)
        parser.add_argument('sid', type=int, required=True, nullable=False)
        parser.add_argument('token', type=str, required=False)
        parser.add_argument(GeetestLib.GEETEST_CHALLENGE, type=str, required=False)
        parser.add_argument(GeetestLib.GEETEST_VALIDATE, type=str, required=False)
        parser.add_argument(GeetestLib.GEETEST_SECCODE, type=str, required=False)
        args = parser.parse_args()

        if app_config.YZM == 'DX':
            # 验证验证码是否正确
            if 'token' not in args:
                abort_msg(403, '顶象验证码已启用，请通过验证码!')
            if not check_yzm_token(args['token']):
                abort_msg(403, '验证码核验失败!')
        elif app_config.YZM == 'geetest':
            # 验证验证码是否正确
            if GeetestLib.GEETEST_CHALLENGE not in args or GeetestLib.GEETEST_VALIDATE not in args or GeetestLib.GEETEST_SECCODE not in args:
                abort_msg(403, 'GeeTest验证码已启用，请通过验证码!')
            challenge = args[GeetestLib.GEETEST_CHALLENGE]
            validate = args[GeetestLib.GEETEST_VALIDATE]
            seccode = args[GeetestLib.GEETEST_SECCODE]
            res = check_geetest(challenge, validate, seccode)
            if not res:
                abort_msg(403, '验证码核验失败!')
        # 验证码正确或未启用验证码，进入正常验证流程
        # 计算pwd的md5值
        pwd = get_pwd(args['sid'], args['passwd'])
        try:
            user = UserOrm.query.filter_by(sid=args['sid'], password=pwd).first()
        except:
            abort_msg(500, '链接数据库失败!')
            return
        if user is None:
            abort_msg(400, '账户或密码错误!')
            return
        # 取出信息放入session
        session['uid'] = user.uid
        session['sid'] = user.sid
        session['name'] = user.name
        # 设置session为永久
        session.permanent = True
        last_login_time = user.last_login_time
        # 更新上次登录时间
        user.last_login_time = str(int(time.time()))
        try:
            db.session.commit()
        except:
            # 只是更新上次登录时间出错而已，问题不大
            db.session.rollback()
        return ret_data({
            'uid': session['uid'],
            'sid': session['sid'],
            'name': session['name'],
            'last_login_time': int(last_login_time)
        })

    def delete(self):
        # 将session全部pop出去
        # 取消掉redis中uid->session映射
        if 'uid' in session:
            r = app_config.utos
            sid = session.sid
            # 重新为redis中uid映射赋值
            try:
                r.delete(str(session['uid']) + '_' + sid)
            except BaseException as e:
                app.logger.warning("用户%d的uid->session从redis删除时失败: %s" % (int(session['uid']), str(e)))
        l = list()
        for i in session:
            if i != '_permanent' and i != 'csrf_token':
                l.append(i)
        for i in l:
            session.pop(i)
        # 同时取消session永久
        session.permanent = False
        return ret_data()

    def get(self):
        if 'uid' in session:
            return ret_data({
                'uid': session['uid'],
                'sid': session['sid'],
                'name': session['name']
            })
        else:
            abort_msg(404, '未登录或登录过期!')
