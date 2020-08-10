from flask_restful import Resource, reqparse, abort
from flask import session
from model import *
import app_config
import time

from tools import *
from app import app


class AnnList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page_index', type=int, default=1)
        args = parser.parse_args()
        page_index = args['page_index']
        try:
            Anns = db.session.query(AnnOrm).filter().slice((page_index - 1) * app_config.page_size,
                                                       page_index * app_config.page_size)
        except BaseException as e:
            app.logger.warning("查询公告%d->%d时失败: %s" % ((page_index - 1) * app_config.page_size,
                                                       page_index * app_config.page_size, str(e)))
            abort_msg(500, '查询公告失败!')
            return
        r_data = list()
        for i in Anns:
            d = {
                'id': i.id,
                'title': i.title,
                'time': int(i.time)
            }
            r_data.append(d)
        try:
            count = db.session.query(AnnOrm).count()
        except BaseException as e:
            app.logger.warning("查询公告数量时失败: %s" % str(e))
            abort_msg(500, '查询公告数量失败!')
            return
        return ret_data({
            'page_size': app_config.page_size,
            'total': count,
            'list': r_data
        })


class Ann(Resource):
    def get(self, aid):
        try:
            ann = AnnOrm.query.get(aid)
        except BaseException as e:
            app.logger.warning("查询公告%d时失败: %s" % (aid, str(e)))
            abort_msg(500, '查询公告失败!')
            return
        return ret_data({
            'id': ann.id,
            'title': ann.title,
            'info': ann.info,
            'time': int(ann.time)
        })
