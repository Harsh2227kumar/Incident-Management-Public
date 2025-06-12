from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class IncidentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], validators=[DataRequired()])
    submit = SubmitField('Create Incident')

class AssignIncidentForm(FlaskForm):
    assigned_to = SelectField('Assign To', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Incident')

class ResolveIncidentForm(FlaskForm):
    resolution_notes = TextAreaField('Resolution Notes', validators=[DataRequired()])
    submit = SubmitField('Resolve Incident') 