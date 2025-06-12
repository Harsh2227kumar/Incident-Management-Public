from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.incidents import bp
from app.models import Incident, User
from app.incidents.forms import IncidentForm, AssignIncidentForm, ResolveIncidentForm
from app.utils.email import send_incident_notification

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = IncidentForm()
    if form.validate_on_submit():
        incident = Incident(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            created_by=current_user.id
        )
        db.session.add(incident)
        db.session.commit()
        send_incident_notification(incident, 'created')
        flash('Your incident has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('incidents/create.html', title='Create Incident', form=form)

@bp.route('/<int:id>')
@login_required
def view(id):
    incident = Incident.query.get_or_404(id)
    if not (current_user.is_admin() or 
            current_user.is_support() and incident.assigned_to == current_user.id or 
            incident.created_by == current_user.id):
        flash('You do not have permission to view this incident.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('incidents/view.html', title='View Incident', incident=incident)

@bp.route('/<int:id>/assign', methods=['GET', 'POST'])
@login_required
def assign(id):
    if not current_user.is_admin():
        flash('You do not have permission to assign incidents.', 'danger')
        return redirect(url_for('main.index'))
    
    incident = Incident.query.get_or_404(id)
    form = AssignIncidentForm()
    form.assigned_to.choices = [(u.id, u.username) for u in User.query.filter_by(role='support').all()]
    
    if form.validate_on_submit():
        incident.assigned_to = form.assigned_to.data
        incident.status = 'in_progress'
        db.session.commit()
        send_incident_notification(incident, 'assigned')
        flash('Incident has been assigned!', 'success')
        return redirect(url_for('incidents.view', id=incident.id))
    return render_template('incidents/assign.html', title='Assign Incident', form=form, incident=incident)

@bp.route('/<int:id>/resolve', methods=['GET', 'POST'])
@login_required
def resolve(id):
    incident = Incident.query.get_or_404(id)
    if not (current_user.is_admin() or 
            current_user.is_support() and incident.assigned_to == current_user.id):
        flash('You do not have permission to resolve this incident.', 'danger')
        return redirect(url_for('main.index'))
    
    form = ResolveIncidentForm()
    if form.validate_on_submit():
        incident.status = 'resolved'
        incident.resolution_notes = form.resolution_notes.data
        db.session.commit()
        send_incident_notification(incident, 'resolved')
        flash('Incident has been resolved!', 'success')
        return redirect(url_for('incidents.view', id=incident.id))
    return render_template('incidents/resolve.html', title='Resolve Incident', form=form, incident=incident) 