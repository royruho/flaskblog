import time
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from flask import current_app
from flask_login import UserMixin
from flaskblog import db, login_manager
from flaskblog.remainders import utils


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    reminders = db.relationship('Reminder', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @classmethod
    def get_num_registered(cls):
        return cls.query.count()

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except BadData:
            return None
        return user_id

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    duration_sec = db.Column(db.Integer, nullable=False)
    date_run = db.Column(db.DateTime, nullable=True)
    run_status = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Reminder('{self.title}', '{self.duration_sec}',{self.run_status})"

    def __call__(self, *args, **kwargs):
        time.sleep(self.duration_sec)
        print(f'reminder {self} was called')
        return self.__repr__()

    def set_reminder(self):
        if self.run_status:
            return False
        print(f"run_reminder user: {User.query.filter_by(id=self.user_id).first()}")
        utils.async_run_reminder(self, User.query.filter_by(id=self.user_id).first())
        self.run_status = True
        self.date_run = datetime.utcnow()
        return True

    def get_status(self):
        return self.run_status
