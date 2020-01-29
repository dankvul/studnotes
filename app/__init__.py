from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

with app.app_context():
    from app.routes.deadline import bp as deadline_bp
    app.register_blueprint(deadline_bp)

with app.app_context():
    from app.routes.login import bp as login_bp
    app.register_blueprint(login_bp)

with app.app_context():
    from app.routes.queue import bp as queue_bp
    app.register_blueprint(queue_bp)

from app.routes import login
from app.routes.login import login
from app.routes import queue
from app.models import users
