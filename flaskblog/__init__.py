from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from flask_executor import Executor

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
executor = Executor()

login_manager = LoginManager()
login_manager.login_view = 'users.login'  # function name of login route
login_manager.login_message_category = 'info'  # bootstrap class for messages

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.remainders.routes import reminders
from flaskblog.main.routes import main
from flaskblog.errors.handlers import errors


def create_app(config_class=Config):
    print("create app")
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    executor.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(reminders)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
