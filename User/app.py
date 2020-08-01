from flask_restful import Resource, reqparse, abort
from flask import session, request
from model import *
import app_config
import time

from tools import *


class User(Resource):
    def get(self, uid=None):
        if not uid:
            if 'uid' not in session:
                abort_msg(401, '未登录或登录过期!')
            else:
                uid = int(session['uid'])
        # 查询uid对应的用户信息
        try:
            user = UserOrm.query.get(uid)
        except:
            abort_msg(500, '数据库连接失败!')
            return
        if not user:
            abort_msg(404, '该用户不存在!')
        if 'uid' in session:
            if uid == int(session['uid']):
                # 输出完整信息
                r_data = {
                        'uid': user.uid,
                        'sid': user.sid,
                        'name': user.name,
                        'reg_time': int(user.reg_time),
                        'try_num': int(user.try_num),
                        'pass_num': int(user.pass_num),
                        'rank': user.rank,
                        'score': user.score,
                        'blog_url': user.blog_url,
                        'signature': user.signature,
                        'true_name': user.true_name,
                        'phone': user.phone
                    }
                if user.u_class:
                    r_data['class_name'] = user.u_class.name
                else:
                    r_data['class_name'] = "暂未加入班级"
                return ret_data(r_data)
        # 输出不完整信息
        r_data = {
            'uid': user.uid,
            'name': user.name,
            'reg_time': int(user.reg_time),
            'try_num': int(user.try_num),
            'pass_num': int(user.pass_num),
            'rank': user.rank,
            'score': user.score,
            'blog_url': user.blog_url,
            'signature': user.signature,
            'class_name': user.u_class.name,
        }
        if user.u_class:
            r_data['class_name'] = user.u_class.name
        else:
            r_data['class_name'] = "暂未加入班级"
        return ret_data(r_data)

    def post(self):
        if 'uid' not in session:
            abort_msg(401, '未登录或登录过期!')
        try:
            user = UserOrm.query.get(session['uid'])
        except:
            abort_msg(500, '数据库连接失败!')
            return
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('blog_url', type=str, required=True)
        parser.add_argument('signature', type=str, required=True)
        parser.add_argument('phone', type=str, required=True)
        args = parser.parse_args()
        if args.get('name') is None:
            abort_msg(403, '昵称不可为空!')
        user.name = args.get('name')
        user.blog_url = args.get('blog_url')
        user.signature = args.get('signature')
        user.phone = args.get('phone')
        try:
            db.session.commit()
        except:
            db.session.rollback()
            abort_msg(500, '数据库连接错误!')
        return self.get()
