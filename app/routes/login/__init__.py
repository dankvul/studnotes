from flask import Blueprint

bp = Blueprint('login', __name__)

from app.routes.login import login