# 🛠️ Incident Manager

A Dockerized Flask application for managing tech support tickets and system incidents. This application provides a complete solution for tracking, managing, and resolving technical incidents with features like user authentication, role-based access control, and email notifications.

## 📑 Table of Contents
- [📌 Project Overview](#project-overview)
- [🏗️ Architecture](#architecture)
- [🧰 Setup and Installation](#setup-and-installation)
- [📁 Project Structure](#project-structure)
- [🧩 Detailed Component Documentation](#detailed-component-documentation)
- [📡 API Documentation](#api-documentation)
- [🗄️ Database Schema](#database-schema)
- [🔐 Security Considerations](#security-considerations)
- [🚀 Deployment Guide](#deployment-guide)
- [🐛 Troubleshooting](#troubleshooting)


## Deliverables
1. Terraform scripts (in the repo)
2. Infrastructure diagram (diagram.png)
3. Screenshots from both cloud dashboards (ss1.png, ss2.png, ss3.png)
4. Deployment report with validation steps (given below)


## 📌 Project Overview (#project-overview)

Incident Manager is a web-based application designed to streamline the process of managing technical incidents and support tickets. It provides a centralized platform for users to report issues, track their status, and receive notifications about updates.

### ✨ Key Features
- ✅ User authentication and authorization
- 🔐 Role-based access control (Admin, Support, Regular User)
- 🔄 Incident lifecycle management
- 📬 Email notifications for incident updates
- 🐳 Docker containerization
- 💾 SQLite database for data persistence
- 🌐 RESTful API endpoints
- 🎨 Bootstrap-based responsive UI

## 🏗️ Architecture

The application follows a modular architecture with the following components:

### 🔙 Backend
- **Framework**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Email**: SMTP with Mailtrap integration
- **Containerization**: Docker

### 🔜 Frontend
- **Framework**: Bootstrap 5
- **Templates**: Jinja2
- **Forms**: Flask-WTF
- **Validation**: WTForms

## 🧰 Setup and Installation

### ⚙️ Prerequisites
- Docker and Docker Compose
- Git
- Python 3.9+ (for local development)

### 🚀 Installation Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd incident-manager
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   ```

3. Update credentials in `.env`:
   ```
   FLASK_APP=run.py
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   MAIL_SERVER=sandbox.smtp.mailtrap.io
   MAIL_PORT=2525
   MAIL_USE_TLS=True
   MAIL_USE_SSL=False
   MAIL_USERNAME=your-mailtrap-username
   MAIL_PASSWORD=your-mailtrap-password
   MAIL_DEFAULT_SENDER=from@example.com
   ```

4. Build and run with Docker:
   ```bash
   docker-compose up --build
   ```

5. Create initial users:
   ```bash
   docker-compose exec web python create_users.py
   ```

## 📁 Project Structure

```
incident-manager/
├── app/
│   ├── __init__.py          
│   ├── models.py            
│   ├── auth/                
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── routes.py
│   │   └── templates/
│   ├── incidents/           
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── routes.py
│   │   └── templates/
│   ├── main/               
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   ├── static/             
│   │   ├── css/
│   │   └── js/
│   └── utils/              
│       └── email.py
├── data/                   
├── instance/              
├── logs/                  
├── tests/                 
├── .env.example          
├── .gitignore            
├── config.py             
├── create_users.py       
├── docker-compose.yml    
├── Dockerfile            
├── requirements.txt      
└── run.py               
```

## 🧩 Detailed Component Documentation

### 1. 🏭 Application Factory (`app/__init__.py`)
```python
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(incidents_bp)
    app.register_blueprint(main_bp)
    
    return app
```

### 2. 🧬 Database Models (`app/models.py`)
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)
    incidents_created = db.relationship('Incident', backref='creator', lazy='dynamic')
    incidents_assigned = db.relationship('Incident', backref='assignee', lazy='dynamic')

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    resolution_notes = db.Column(db.Text)
```

### 3. 🔐 Authentication (`app/auth/`)

#### Forms (`forms.py`)
```python
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
```

#### Routes (`routes.py`)
```python
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Sign In', form=form)
```

### 4. 🧾 Incidents Management (`app/incidents/`)

#### Forms (`forms.py`)
```python
class IncidentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])
    submit = SubmitField('Submit')
```

#### Routes (`routes.py`)
```python
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
        flash('Your incident has been created.')
        return redirect(url_for('incidents.index'))
    return render_template('incidents/create.html', title='Create Incident', form=form)
```

### 5. 📬 Email Notifications (`app/utils/email.py`)
```python
def send_incident_notification(incident, action):
    if not current_app.config['MAIL_USERNAME']:
        return
    
    creator = User.query.get(incident.created_by)
    assignee = User.query.get(incident.assigned_to) if incident.assigned_to else None
    
    if action == 'created':
        recipients = [u.email for u in User.query.filter_by(role='admin').all()]
        subject = f'New Incident Created: {incident.title}'
        body = f"""
        New incident created:
        Title: {incident.title}
        Priority: {incident.priority}
        Created by: {creator.username}
        Description: {incident.description}
        """
```

### 6. ⚙️ Configuration (`config.py`)
```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'sandbox.smtp.mailtrap.io')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 2525))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
```

### 7. 🐳 Docker Configuration

#### Dockerfile
```dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/instance /app/data
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
```

#### docker-compose.yml
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
      - ./data:/app/data
    environment:
      - FLASK_APP=run.py
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key-here
      - MAIL_SERVER=sandbox.smtp.mailtrap.io
      - MAIL_PORT=2525
      - MAIL_USE_TLS=True
      - MAIL_USE_SSL=False
      - MAIL_USERNAME=your-mailtrap-username
      - MAIL_PASSWORD=your-mailtrap-password
      - MAIL_DEFAULT_SENDER=from@example.com
```

## 📡 API Documentation

### 🔐 Authentication Endpoints
- `POST /login`: User login
- `POST /logout`: User logout
- `POST /register`: User registration

### 📄 Incident Endpoints
- `GET /incidents`: List all incidents
- `POST /incidents`: Create new incident
- `GET /incidents/<id>`: Get incident details
- `PUT /incidents/<id>`: Update incident
- `DELETE /incidents/<id>`: Delete incident
- `POST /incidents/<id>/assign`: Assign incident
- `POST /incidents/<id>/resolve`: Resolve incident

## 🗄️ Database Schema

### 👤 Users Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    role VARCHAR(20) NOT NULL
);
```

### 🧾 Incidents Table
```sql
CREATE TABLE incident (
    id INTEGER PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER NOT NULL,
    assigned_to INTEGER,
    resolution_notes TEXT,
    FOREIGN KEY (created_by) REFERENCES user (id),
    FOREIGN KEY (assigned_to) REFERENCES user (id)
);
```


## 🚀 Deployment Guide

### 🏭 Production Deployment
1. Set up a production database (PostgreSQL recommended)
2. Configure a production email service
3. Use a production WSGI server (NGINX)

### 🔧 Environment Variables
- `FLASK_ENV`: Set to 'production'
- `SECRET_KEY`: Generate a secure random key
- `DATABASE_URL`: Production database URL
- `MAIL_*`: Production email settings

## 🐛 Troubleshooting

### ⚠️ Common Issues
1. **Database Connection Issues**
   - Database permissions
   - Database configuration

2. **Email Sending Issues**
   - SMTP settings
   - Email credentials

3. **Authentication Issues**
   - User credentials
   - Session configuration

### 📝 Logging
- Application logs in `logs/incident_manager.log`
- Docker logs: `docker-compose logs web`
- Database logs: Check database configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request



## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Default Users

The application comes with these default users:
- Admin: admin@example.com / admin123
- Support: support@example.com / support123
- User: user@example.com / user123

## 🔒 Security Notes

Before deploying to production:
1. Change all default credentials
2. Use a proper production database
3. Configure a production email service
4. Set up proper SSL/TLS
