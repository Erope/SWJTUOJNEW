from app import db


class UserOrm(db.Model):
    __tablename__ = 'user'

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    sid = db.Column(db.BIGINT, nullable=False)
    password = db.Column(db.VARCHAR(32), nullable=False)
    name = db.Column(db.VARCHAR(20), default="默认昵称", nullable=False)
    reg_time = db.Column(db.CHAR(10), nullable=False)
    last_login_time = db.Column(db.CHAR(10), default="0", nullable=False)
    try_num = db.Column(db.Integer, default=0, nullable=False)
    pass_num = db.Column(db.Integer, default=0, nullable=False)
    rank = db.Column(db.Integer, default=-1, nullable=False)
    blog_url = db.Column(db.VARCHAR(40), default="",  nullable=False)
    signature = db.Column(db.VARCHAR(255), default="", nullable=False)
    class_id = db.Column(db.Integer)
    true_name = db.Column(db.VARCHAR(30), default='请联系管理员更改真实姓名', nullable=False)
    phone = db.Column(db.CHAR(11))


    def __repr__(self):
        return '%s-->%s' % (self.name, self.studentid)

