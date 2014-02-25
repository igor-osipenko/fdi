from database import db
import hashlib
from datetime import datetime

ROLE_USER = 1
ROLE_OPERATOR = 2
ROLE_ADMIN = 3

class Role(db.Model):
    __tablename__ = u'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return str(self.name)


class User(db.Model):
    __tablename__ = u'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=ROLE_USER)
    email = db.Column(db.String(50), unique=True)

    username = db.Column(db.String(50))
    password = db.Column(db.String(128))
    registration_date = db.Column(db.DateTime, default=datetime.now())
    gmt = db.Column(db.Float, default=0.0)

    role = db.relationship('Role', backref='users', lazy='joined')

    def __init__(self, rid=ROLE_USER, e=None, un=None, psw=None, rdate=None, gmt=None):
        self.role_id = rid
        self.email = e
        self.username = un
        self.password = psw
        self.registration_date = rdate
        self.gmt = gmt

    def __setattr__(self, key, value):
        if key == 'password' and value:
            object.__setattr__(self, key, hashlib.sha512(value).hexdigest())
        else:
            object.__setattr__(self, key, value)

    def __repr__(self):
        return self.email


class Subject(db.Model):
    __tablename__ = u'subjects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Subject %r>' % self.name

    def __str__(self):
        return str(self.name)


class Category(db.Model):
    __tablename__ = u'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    name = db.Column(db.String(25), unique=True)

    subject = db.relationship('Subject', backref='categories', lazy='joined')

    def __init__(self, name=None, subject_id=None):
        self.name = name
        self.subject_id = subject_id

    def __repr__(self):
        return '<Category %r>' % self.name

    def __str__(self):
        return str(self.name)


class OS(db.Model):
    __tablename__ = 'os'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16))

    def __init__(self, n=None):
        self.name = n

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


class TaskStatus(db.Model):
    __tablename__ = 'task_statuses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(256))

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

    def __init__(self, n=None, descr=None):
        self.name = n
        self.description = descr


class Order(db.Model):
    __tablename__ = 'orders'
    id =            db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id =       db.Column(db.Integer, db.ForeignKey('users.id'))
    subject_id =    db.Column(db.Integer, db.ForeignKey('subjects.id'))
    category_id =   db.Column(db.Integer, db.ForeignKey('categories.id'))
    os_id =         db.Column(db.Integer, db.ForeignKey('os.id'))
    status_id =     db.Column(db.Integer, db.ForeignKey('task_statuses.id'), default=1)

    title =         db.Column(db.String(30))
    deadline =      db.Column(db.String(16))
    details =       db.Column(db.String(2048))
    explanations =  db.Column(db.Boolean)
    submit_date =   db.Column(db.DateTime, default=datetime.now())
    price =         db.Column(db.Float, default=0.0)
    is_deleted =    db.Column(db.Boolean, default=False)
    is_rated =      db.Column(db.Boolean, default=False)

    subject =       db.relationship('Subject', backref='order', lazy='joined')
    category =      db.relationship('Category', backref='order', lazy='joined')
    status =        db.relationship('TaskStatus', backref='order', lazy='joined')
    user =          db.relationship('User', backref='order', lazy='joined')
    os =            db.relationship('OS', backref='order', lazy='joined')


    def __init__(self, uid=None, t=None, sid=None, cid=None, oid=None, dl=None, dt=None, ex=None, sd=None, pr=None,
                 dbu=None, stid=None, r=None):

        self.user_id = uid
        self.subject_id = sid
        self.category_id = cid
        self.os_id = oid
        self.status_id = stid
        self.title = t
        self.deadline = dl
        self.details = dt
        self.explanations = ex
        self.submit_date = sd
        self.price = pr
        self.is_deleted = dbu
        self.is_rated = r

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    name = db.Column(db.String(255))
    local_name = db.Column(db.String(255))

    order = db.relationship('Order', backref='file', lazy='joined')

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)