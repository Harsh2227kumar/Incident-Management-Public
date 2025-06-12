from app import create_app, db
from app.models import User
import os

def create_temporary_users():
    app = create_app()
    with app.app_context():
        # Create admin user
        admin = User(
            username=os.environ.get('ADMIN_USERNAME', 'admin'),
            email=os.environ.get('ADMIN_EMAIL', 'admin@example.com'),
            role='admin'
        )
        admin.set_password(os.environ.get('ADMIN_PASSWORD', 'admin123'))

        # Create support user
        support = User(
            username=os.environ.get('SUPPORT_USERNAME', 'support'),
            email=os.environ.get('SUPPORT_EMAIL', 'support@example.com'),
            role='support'
        )
        support.set_password(os.environ.get('SUPPORT_PASSWORD', 'support123'))

        # Create regular user
        user = User(
            username=os.environ.get('USER_USERNAME', 'user'),
            email=os.environ.get('USER_EMAIL', 'user@example.com'),
            role='user'
        )
        user.set_password(os.environ.get('USER_PASSWORD', 'user123'))

        # Add users to database
        db.session.add(admin)
        db.session.add(support)
        db.session.add(user)
        db.session.commit()

        print("Temporary users created successfully!")
        print("\nLogin Credentials:")
        print("------------------")
        print("Admin:")
        print(f"Email: {admin.email}")
        print(f"Password: {os.environ.get('ADMIN_PASSWORD', 'admin123')}")
        print("\nSupport:")
        print(f"Email: {support.email}")
        print(f"Password: {os.environ.get('SUPPORT_PASSWORD', 'support123')}")
        print("\nRegular User:")
        print(f"Email: {user.email}")
        print(f"Password: {os.environ.get('USER_PASSWORD', 'user123')}")

if __name__ == '__main__':
    create_temporary_users() 