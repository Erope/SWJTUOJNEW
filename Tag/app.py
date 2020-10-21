from flask_restful import Resource
from model import *
from tools import *


class Tag(Resource):
    def __init__(self):
        if 'uid' not in session:
            abort_msg(401, '未登录或登录过期!')

    def get(self, level, father=None):
        if level >= 2 and father is None:
            abort_msg(403, '二级及以上标签应给出父标签!')
        tags = db.session.query(TagOrm).filter(TagOrm.tag_level == level, TagOrm.tag_father == father).all()
        l = list()
        for tag in tags:
            l.append({
                'tid': tag.tag_id,
                'name': tag.tag_text
            })
        return ret_data(l)


class TagChooseQu(Resource):
    def __init__(self):
        if 'uid' not in session:
            abort_msg(401, '未登录或登录过期!')

    def get(self, tid, level):
        # 跳过查询是否有权限获取题目步骤
        # 进行随机抽取并排序
        # EXPLAIN下看起来速度还行，如果后期出现瓶颈再考虑修复
        # EXPLAIN: qu表未使用索引，order_by进行随机排序使用了临时表
        # qu = QuOrm.query.filter(QuOrm.tags.any(TagOrm.tag_id == tid),
        #                        QuOrm.qu_level == level).order_by(db.text('RAND()')).first()
        qu = db.session.query(QuOrm).join(tagmap).filter(QuOrm.qu_level == level,
                                                         TagOrm.tag_id == tid).order_by(db.text('RAND()')).first()
        if qu is None:
            abort_msg(404, '标签不存在或题库无可用题')
        return ret_data(qu.qu_id)
