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
    score = db.Column(db.Integer, default=0, nullable=False)
    blog_url = db.Column(db.VARCHAR(40), default="",  nullable=True)
    signature = db.Column(db.VARCHAR(255), default="", nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.cid'))
    true_name = db.Column(db.VARCHAR(30), default='请联系管理员更改真实姓名', nullable=False)
    phone = db.Column(db.CHAR(11))

    u_class = db.relationship('ClassOrm', backref=db.backref('students'))

    def __repr__(self):
        return '%s-->%s' % (self.name, self.studentid)


class ClassOrm(db.Model):
    __tablename__ = 'class'

    cid = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.VARCHAR(250), nullable=True)
    tid = db.Column(db.Integer, nullable=True)
    join_pwd = db.Column(db.VARCHAR(100), nullable=True)
    f_cid = db.Column(db.Integer, db.ForeignKey('class.cid'), nullable=True)


class AnnOrm(db.Model):
    __tablename__ = 'announcement'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.VARCHAR(512), nullable=False, default='无标题')
    info = db.Column(db.Text, nullable=False)
    time = db.Column(db.CHAR(10), nullable=False)
