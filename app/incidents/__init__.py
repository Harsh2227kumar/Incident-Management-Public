from flask import Blueprint

bp = Blueprint('incidents', __name__)

from app.incidents import routes 