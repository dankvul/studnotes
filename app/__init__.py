from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


migrate = Migrate()
db = SQLAlchemy()
loginn = LoginManager()
loginn.login_view = 'login'


def getApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    loginn.init_app(app=app)

    with app.app_context():
        from app.routes.deadline import bp as deadline_bp
        app.register_blueprint(deadline_bp)

    with app.app_context():
        from app.routes.login import bp as login_bp
        app.register_blueprint(login_bp)

    with app.app_context():
        from app.routes.queue import bp as queue_bp
        app.register_blueprint(queue_bp)
    return app


from app.routes import login
from app.routes.login import login
from app.routes import queue
from app.models import users
