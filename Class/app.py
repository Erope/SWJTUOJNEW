from flask_restful import Resource, reqparse, abort
from flask import session
from model import *
import app_config
import time
import base64
from tools import *
from app import app


class ClassInfo(Resource):
    def __init__(self):
        if 'uid' not in session:
            abort_msg(401, '未登录或登录过期!')

    def get(self):
        uid = session.get('uid')
        try:
            u = UserOrm.query.get(uid)
        except BaseException as e:
            abort_msg(500, '数据库连接失败!')
            app.logger.warning("数据库连接失败: %s" % str(e))
            return
        if u is None:
            app.logger.warning("本应存在的用户返回不存在: %d" % uid)
            abort_msg(404, '用户不存在')
            return
        c = u.u_class
        if c is None:
            abort_msg(404, '您还没有加入班级!')
            return
        # 求出全班的平均分数
        try:
            avg_score, avg_pass, avg_Qscore = db.session.query\
                (db.func.AVG(UserOrm.score), db.func.AVG(UserOrm.pass_num), db.func.AVG(UserOrm.Qscore))\
                .filter(UserOrm.class_id == c.cid).one()
        except BaseException as e:
            app.logger.warning("查询班级平均分数时，数据库错误: %s" % str(e))
            abort_msg(500, '数据库错误!')
            return
        data = {
            'name': c.name,
            'score': u.score,
            'avg_score': float(avg_score),
            'avg_pass': float(avg_pass),
            'avg_Qscore': float(avg_Qscore)
        }
        return ret_data(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('pwd', type=str, required=True)
        args = parser.parse_args()
        pwd = args['pwd']
        uid = session.get('uid')
        u = UserOrm.query.get(uid)
        try:
            c_name, c_cid = db.session.query(ClassOrm.name, ClassOrm.cid).filter(ClassOrm.join_pwd == pwd).one()
        except:
            abort_msg(404, '无法查询到对应班级!请核对邀请码!')
            return
        u.class_id = int(c_cid)
        try:
            db.session.commit()
        except BaseException as e:
            app.logger.warning("加入班级时，数据库错误: %s" % str(e))
            abort_msg(500, '加入班级时出错!')
            return
        data = {
            'msg': '班级绑定成功!',
            'name': c_name
        }
        return ret_data(data)
