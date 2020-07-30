from flask import Flask
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
