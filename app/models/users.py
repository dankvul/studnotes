from app import db
from flask_login import UserMixin
from app import loginn as login
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import randomString


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    password_hash = db.Column(db.String(128))
    tg_id = db.Column(db.Integer)
    role = db.Column(db.Boolean)  # 0 -- user, 1 -- headmaster

    def make_headmaster(self):
        self.role = 1
        db.session.commit()

    def change_password(self, new_pass):
        self.password_hash = generate_password_hash(new_pass)
        db.session.commit()

    def set_group_id(self, token):
        g = Group.query.filter_by(reg_token=token).first()
        if g:
            self.group_id = g.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Username {}>\n<id {}>".format(self.username, self.id)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_token = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(32))

    def set_token(self):
        new_token = randomString(32)
        while Group.query.filter_by(reg_token=new_token).first():
            new_token = randomString(32)
        self.reg_token = new_token

    def __repr__(self):
        return '<Class Group: group {}>\n<token {}>'.format(self.name, self.reg_token)


class Deadline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    exp_date = db.Column(db.Date)
    body = db.Column(db.String)
    state = db.Column(db.Boolean)  # hard == true, soft == false

    def set_group_id(self, g: Group):
        self.group_id = g.id

    def __repr__(self):
        return '<Class Deadline: date {}, group_id {}, state {}>'.format(self.exp_date, self.group_id, self.state)


class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    queue_name = db.Column(db.String(128))

    def get_size(self):
        lst = QueueMember.query.filter_by(queue_id=self.id).all()
        return len(lst)

    def __str__(self):
        return "<Class queue: id {}, group_id {}, queue_name {}".format(self.id, self.group_id, self.queue_name)


class QueueMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    queue_id = db.Column(db.Integer, db.ForeignKey('queue.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
