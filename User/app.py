from flask_restful import Resource, reqparse
from flask import request
from werkzeug.utils import secure_filename
from model import *
from PIL import Image
import os
from app import app
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
        except BaseException as e:
            abort_msg(500, '数据库连接失败!')
            app.logger.warning("数据库连接失败: %s" % str(e))
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
                        'Qscore': user.Qscore,
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
        else:
            r_data = {
                'uid': user.uid,
                'name': user.name,
                'reg_time': int(user.reg_time),
                'try_num': int(user.try_num),
                'pass_num': int(user.pass_num),
                'rank': user.rank,
                'score': user.score,
                'Qscore': user.Qscore,
                'blog_url': user.blog_url,
                'signature': user.signature,
                'class_name': user.u_class.name,
            }
            if user.u_class:
                r_data['class_name'] = user.u_class.name
            else:
                r_data['class_name'] = "暂未加入班级"
            return ret_data(r_data)

    def put(self):
        if 'uid' not in session:
            abort_msg(401, '未登录或登录过期!')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('blog_url', type=str, required=True)
        parser.add_argument('signature', type=str, required=True)
        parser.add_argument('phone', type=str, required=True)
        args = parser.parse_args()
        if args.get('name') is None:
            abort_msg(403, '昵称不可为空!')
        try:
            user = UserOrm.query.get(session['uid'])
        except BaseException as e:
            abort_msg(500, '数据库连接失败!')
            app.logger.warning("数据库连接失败: %s" % str(e))
            return
        user.name = args.get('name')
        user.blog_url = args.get('blog_url')
        user.signature = args.get('signature')
        user.phone = args.get('phone')
        try:
            db.session.commit()
        except BaseException as e:
            db.session.rollback()
            abort_msg(500, '更新个人资料失败!')
            app.logger.warning("数据库更新个人资料失败: %s" % str(e))
            return
        return self.get()


def SaveSizePic(name, file, size=None):
    try:
        im = Image.open(file)
        if size is not None:
            im.thumbnail(size)
    except BaseException as e:
        app.logger.warning("图片解析失败: %s" % str(e))
        abort_msg(500, '图片解析失败!')
        return
    filename = secure_filename(name)
    try:
        im.save(os.path.join(app_config.Avatar_Folder, filename))
    except BaseException as e:
        app.logger.warning("文件写入服务器失败: %s" % str(e))
        abort_msg(500, '头像文件写入服务器失败!')


class Avatar(Resource):
    def __init__(self):
        if 'uid' not in session:
            abort_msg(401, '未登录或登录过期!')
            return

    def post(self):
        file = request.files.get('file')
        if file is None:
            abort_msg(400, '您必须上传图片!')
            return
        SaveSizePic(str(session['uid'])+'_L.png', file, (512, 512))
        SaveSizePic(str(session['uid']) + '_M.png', file, (256, 256))
        SaveSizePic(str(session['uid']) + '_S.png', file, (128, 128))
        SaveSizePic(str(session['uid']) + '.png', file)
        return ret_data(status=204)


class PWD(Resource):
    def __init__(self):
        if 'uid' not in session:
            abort_msg(401, '未登录或登录过期!')
            return

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('o_pwd', type=str, required=True)
        parser.add_argument('n_pwd', type=str, required=True)
        args = parser.parse_args()
        try:
            user = UserOrm.query.get(session['uid'])
        except BaseException as e:
            app.logger.warning("数据库连接失败: %s" % str(e))
            abort_msg(500, '数据库连接失败!')
            return
        if user is None:
            app.logger.warning("用户不存在: %d" % session.get('uid'))
            abort_msg(500, '数据库连接失败!')
            return
        if user.password != get_pwd(user.sid, args['o_pwd']):
            abort_msg(403, '原密码错误!')
        user.password = get_pwd(user.sid, args['n_pwd'])
        try:
            db.session.commit()
        except BaseException as e:
            app.logger.warning("用户%d修改密码数据库错误: %s" % (int(session['uid']), str(e)))
            db.session.rollback()
            abort_msg(500, '数据库连接错误!')
        # 更新session，删除所有已经登录账户的session
        try:
            r = app_config.utos
            r_s = app_config.r
            for i in r.keys(pattern="%d_*" % int(session['uid'])):
                sid = i[i.find('_') + 1:]
                r.delete("%d_%s" % (int(session['uid']), sid))
                r_s.delete(app.config.get('SESSION_KEY_PREFIX', 'session:') + sid)
            # 使他自己也退出登录
            session.clear()
        except BaseException as e:
            app.logger.warning("用户%d修改密码后踢出所有session失败: %s" % (int(session['uid']), str(e)))
        return ret_data(status=204)
