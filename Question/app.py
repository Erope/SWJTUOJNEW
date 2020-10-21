from flask_restful import Resource, reqparse
from model import *
from tools import *
from app import app


class Qu(Resource):
    def __init__(self):
        if 'uid' not in session:
            abort_msg(401, '未登录或登录过期!')

    def get(self, qid):
        # 跳过查询是否有权限获取题目步骤
        try:
            qu = QuOrm.query.get(qid)
        except BaseException as e:
            app.logger.warning("数据库连接失败: %s" % str(e))
            abort_msg(500, '数据库连接失败!')
            return
        if qu is None:
            abort_msg(404, '题目不存在!')
        d_tag = list()
        for tag in qu.tags:
            d_tag.append({'id': tag.tag_id, 'name': tag.tag_text})
        d_example = list()
        for example in qu.examples:
            d_example.append({'in': example.eg_in, 'out': example.eg_out})
        data = {
            'title': qu.qu_title,
            'content': qu.qu_content,
            'in': qu.qu_in_format,
            'out': qu.qu_out_format,
            'level': qu.qu_level,
            'num': [
                {'name': 'Accept', 'value': qu.qu_ac_num},
                {'name': 'Wrong Answer', 'value': qu.qu_wa_num},
                {'name': 'Time Limit Exceeded', 'value': qu.qu_tle_num},
                {'name': 'Memory Limit Exceeded', 'value': qu.qu_mle_num},
                {'name': 'Presentation ERROR', 'value': qu.qu_pe_num},
                {'name': 'Runtime ERROR', 'value': qu.qu_re_num},
                {'name': 'Compile ERROR', 'value': qu.qu_ce_num}
            ],
            'tag': d_tag,
            'example': d_example,
            'languageOptions': app_config.languageOptions
        }
        return ret_data(data)


class Judge(Resource):
    def __init__(self):
        if 'uid' not in session:
            abort_msg(401, '未登录或登录过期!')

    def get(self, jid=None):
        # 当指定了jid时
        if jid is not None:
            jd = JudgeOrm.query.get(jid)
            if jd is None:
                abort_msg(404, '判题不存在')
            if jd.uid != session.get('uid'):
                abort_msg(403, '您不拥有此判题记录!')
            # 获取题目信息
            try:
                qu = QuOrm.query.get(jd.qu_id)
            except BaseException as e:
                app.logger.warning("数据库连接失败: %s" % str(e))
                abort_msg(500, '数据库连接错误!')
                return
            if qu is None:
                abort_msg(404, '题目不存在')
            # 返回判题记录
            data = {
                'id': jd.id,
                'qu_id': jd.qu_id,
                'qu_title': qu.qu_title,
                'coding': jd.coding,
                'status': jd.status,
                'error_msg': jd.error_msg,
                'time': jd.time,
                'lan': app_config.languageOptions[jd.lan]['value'],
                'error_testid': jd.error_testid,
                'error_out': jd.error_out
            }
            return ret_data(data)
        else:
            # 查询整个判题记录，需要分页
            parser = reqparse.RequestParser()
            parser.add_argument('page_index', type=int, default=1)
            args = parser.parse_args()
            page_index = args['page_index']
            # 公告分页，分页长度在config中
            try:
                Judges = db.session.query(JudgeOrm).filter(JudgeOrm.uid == session['uid']).\
                    slice((page_index - 1) * app_config.page_size, page_index * app_config.page_size)
            except BaseException as e:
                app.logger.warning("查询判题记录%d->%d时失败: %s" % ((page_index - 1) * app_config.page_size,
                                                          page_index * app_config.page_size, str(e)))
                abort_msg(500, '查询判题记录失败!')
                return
            # 查询题目
            Qu_ids = [i.qu_id for i in Judges]
            try:
                Qus = db.session.query(QuOrm).filter(QuOrm.qu_id.in_(Qu_ids))
            except BaseException as e:
                app.logger.warning("查询题目时失败: %s" % str(e))
                abort_msg(500, '数据库错误!')
                return
            r_data = dict()
            r_data['Judge'] = list()
            for jd in Judges:
                d = {
                    'id': jd.id,
                    'qu_id': jd.qu_id,
                    'status': jd.status,
                    'time': jd.time,
                    'lan': app_config.languageOptions[jd.lan]['value'],
                }
                r_data['Judge'].append(d)
            r_data['Qu'] = list()
            for qu in Qus:
                d_tag = list()
                for tag in qu.tags:
                    d_tag.append({'id': tag.tag_id, 'name': tag.tag_text})
                d = {
                    'id': qu.qu_id,
                    'title': qu.qu_title,
                    'level': qu.qu_level,
                    'num': [
                        {'name': 'Accept', 'value': qu.qu_ac_num},
                        {'name': 'Wrong Answer', 'value': qu.qu_wa_num},
                        {'name': 'Time Limit Exceeded', 'value': qu.qu_tle_num},
                        {'name': 'Memory Limit Exceeded', 'value': qu.qu_mle_num},
                        {'name': 'Presentation ERROR', 'value': qu.qu_pe_num},
                        {'name': 'Runtime ERROR', 'value': qu.qu_re_num},
                        {'name': 'Compile ERROR', 'value': qu.qu_ce_num}
                    ],
                    'tag': d_tag
                }
                r_data['Qu'].append(d)
            try:
                count = db.session.query(JudgeOrm).filter(JudgeOrm.uid == session['uid']).count()
            except BaseException as e:
                app.logger.warning("查询判题数量时失败: %s" % str(e))
                abort_msg(500, '查询判题数量失败!')
                return
            return ret_data({
                'page_size': app_config.page_size,
                'total': count,
                'list': r_data
            })

