from flask_restful import Resource, reqparse, abort
from flask import session
from model import *
import app_config
import time

from tools import *


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
        args = parser.parse_args()
        if app_config.YZM:
            # 验证验证码是否正确
            if 'token' not in args:
                abort_msg(403, '验证码已启用，请通过验证码!')
            if not check_yzm_token(args['token']):
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
        session.clear()
        return ret_data()

    def get(self):
        print(generate_csrf())
        if 'uid' in session:
            return ret_data({
                'uid': session['uid'],
                'sid': session['sid'],
                'name': session['name']
            })
        else:
            abort_msg(404, '未登录或登录过期!')
