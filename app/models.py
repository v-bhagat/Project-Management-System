from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db, login_manager  # Ensure this import is correct

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Assuming this exists
    creator = db.relationship('User', backref='projects_created')  # This sets up the relationship

    def __repr__(self):
        return f"Project('{self.title}', '{self.date_created}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    role = db.Column(db.String(10), nullable=False, default='employee')  # Role can be 'admin' or 'employee'

    # Relationships for tasks
    tasks_assigned = db.relationship('Task', foreign_keys='Task.assigned_to', backref='assignee', lazy=True)
    tasks_created = db.relationship('Task', foreign_keys='Task.created_by', backref='creator', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)  # Link to Project
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)  # Track completion

    def __repr__(self):
        return f"Task('{self.title}', '{self.date_created}', Completed: {self.completed})"