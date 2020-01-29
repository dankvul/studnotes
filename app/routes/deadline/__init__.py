from flask import Blueprint

bp = Blueprint('deadline', __name__,
                     template_folder='templates')

from app.routes.deadline import deadline
