from app import create_app, db
from app.models import Incident, User
from datetime import datetime

def create_sample_incidents():
    app = create_app()
    with app.app_context():
        # Get users
        admin = User.query.filter_by(username='admin').first()
        support = User.query.filter_by(username='support').first()
        user = User.query.filter_by(username='user').first()

        # Create sample incidents
        incidents = [
            {
                'title': 'Server Down',
                'description': 'Production server is not responding to requests.',
                'priority': 'high',
                'status': 'open',
                'created_by': user.id
            },
            {
                'title': 'Database Connection Issue',
                'description': 'Unable to connect to the main database.',
                'priority': 'high',
                'status': 'in_progress',
                'created_by': user.id,
                'assigned_to': support.id
            },
            {
                'title': 'UI Bug in Dashboard',
                'description': 'Dashboard charts are not displaying correctly.',
                'priority': 'medium',
                'status': 'resolved',
                'created_by': user.id,
                'assigned_to': support.id,
                'resolution_notes': 'Fixed by updating the chart library version.'
            },
            {
                'title': 'Login Page Slow',
                'description': 'Login page takes more than 5 seconds to load.',
                'priority': 'medium',
                'status': 'open',
                'created_by': user.id
            }
        ]

        for incident_data in incidents:
            incident = Incident(**incident_data)
            db.session.add(incident)

        db.session.commit()
        print("Sample incidents created successfully!")

if __name__ == '__main__':
    create_sample_incidents() 