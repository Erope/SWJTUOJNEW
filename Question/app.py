from flask_restful import Resource, reqparse, abort
from flask import session
from model import *
import app_config
import time

from tools import *
from app import app


class Qu(Resource):
    def __init__(self):
        if 'uid' not in session:
            abort_msg(401, '未登录或登录过期!')

    def get(self, qid):
        # 跳过查询是否有权限获取题目步骤
        qu = QuOrm.query.get(qid)
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
            'num': {
                'ac_num': qu.qu_ac_num,
                'wa_num': qu.qu_wa_num,
                'tle_num': qu.qu_tle_num,
                'mle_num': qu.qu_mle_num,
                'pe_num': qu.qu_pe_num,
                're_num': qu.qu_re_num,
                'ce_num': qu.qu_ce_num,
            },
            'tag': d_tag,
            'example': d_example,
            'languageOptions': app_config.languageOptions
        }
        return ret_data(data)
