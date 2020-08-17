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


tagmap = db.Table('tagmap', db.metadata,
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id')),
    db.Column('qu_id', db.Integer, db.ForeignKey('question.qu_id')),
)

class ExampleOrm(db.Model):
    __tablename__ = 'io_example'
    __bind_key__ = 'qu'

    eg_id = db.Column(db.Integer, primary_key=True)
    eg_in = db.Column(db.Text)
    eg_out = db.Column(db.Text)
    qu_id = db.Column(db.Integer, db.ForeignKey('question.qu_id'))

    qu = db.relationship('QuOrm', back_populates="examples")

class QuOrm(db.Model):
    __tablename__ = 'question'
    __bind_key__ = 'qu'

    qu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qu_title = db.Column(db.VARCHAR(120))
    qu_content = db.Column(db.Text)
    qu_in_format = db.Column(db.Text)
    qu_out_format = db.Column(db.Text)
    qu_level = db.Column(db.Integer)
    qu_deleted = db.Column(db.Integer)
    qu_ac_num = db.Column(db.Integer)
    qu_wa_num = db.Column(db.Integer)
    qu_ce_num = db.Column(db.Integer)
    qu_tle_num = db.Column(db.Integer)
    qu_mle_num = db.Column(db.Integer)
    qu_pe_num = db.Column(db.Integer)
    qu_re_num = db.Column(db.Integer)
    qu_creator = db.Column(db.Integer)
    qu_create_time = db.Column(db.DateTime)
    qu_time_lmt = db.Column(db.Integer)
    qu_memory_lmt = db.Column(db.Integer)

    tags = db.relationship('TagOrm', secondary=tagmap, back_populates="qus")
    examples = db.relationship('ExampleOrm', backref=db.backref('qus'))


class TagOrm(db.Model):
    __tablename__ = 'tag'
    __bind_key__ = 'qu'

    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_text = db.Column(db.String)
    tag_level = db.Column(db.Integer)
    tag_father = db.Column(db.Integer, db.ForeignKey('tag.tag_id'))

    tag_sons = db.relationship('TagOrm', back_populates='father')
    father = db.relationship('TagOrm', back_populates='tag_sons', remote_side=[tag_id])
    qus = db.relationship('QuOrm', secondary=tagmap, back_populates="tags")


class UserQuMapOrm(db.Model):
    __tablename__ = 'userqumap'

    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True, nullable=False)
    qid = db.Column(db.Integer, db.ForeignKey('question.qu_id'), primary_key=True, nullable=False)
    time = db.Column(db.BIGINT, primary_key=True, nullable=False)
    status = db.Column(db.Integer, default=0, nullable=False)

    user = db.relationship("UserOrm", backref="choosequs")
    qu = db.relationship("QuOrm")
