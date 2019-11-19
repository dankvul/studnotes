from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import randomString


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    password_hash = db.Column(db.String(128))

    def set_group_id(self, token):
        g = Group.query.filter_by(reg_token=token).first()
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
        return '<group {}>\n<token {}>'.format(self.name, self.reg_token)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))