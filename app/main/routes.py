from flask import render_template
from flask_login import login_required, current_user
from app.main import bp
from app.models import Incident

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    if current_user.is_admin():
        incidents = Incident.query.all()
    elif current_user.is_support():
        incidents = Incident.query.filter_by(assigned_to=current_user.id).all()
    else:
        incidents = Incident.query.filter_by(created_by=current_user.id).all()
    return render_template('main/index.html', title='Home', incidents=incidents) 