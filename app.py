from flask import Flask, session
from flask_restful import Resource, Api
from flask_session import Session
import app_config
from werkzeug.middleware.proxy_fix import ProxyFix
import url_table
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(app_config)
app.wsgi_app = ProxyFix(app.wsgi_app)
Session(app)
if app_config.CSRF_Token:
    CSRFProtect(app)
api = Api(app)
db = SQLAlchemy()
db.init_app(app)
url_table.init_url()
app.logger.addHandler(app_config.handler)


# 注册redis的session延期
@app.after_request
def call_after_request_callbacks(response):
    # 检查用户是否已经登录
    if 'uid' in session:
        # 每次调用后会增加登录用户redis保存时间
        r = app_config.utos
        # 取出当前sid
        sid = session.sid
        # 重新为redis中uid映射赋值
        try:
            r.set(str(session['uid']) + '_' + sid, sid, ex=app_config.PERMANENT_SESSION_LIFETIME)
            print('OK!')
        except BaseException as e:
            app.logger.warning("用户%d的uid->session映射写入redis时失败: %s" % (int(session['uid']), str(e)))
    return response
