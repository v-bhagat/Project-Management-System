from flask import render_template, url_for, flash, redirect, request  
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint
from functools import wraps
from app.models import User, Task, Project  # Ensure Task is imported

main = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('You do not have permission to perform this action.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@main.route("/")
@main.route("/dashboard")
@login_required
def dashboard():
    projects = Project.query.all()  # Fetch all projects
    return render_template('dashboard.html', title='Dashboard', projects=projects)

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard')) 

    print('Registering user')
    form = RegistrationForm()

    if form.validate_on_submit():
        # Check if the email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('main.login'))  # Redirect to the login page if the email exists

        # Proceed to create a new user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', title='Register', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    users = User.query.all()  # Get all users
    projects = Project.query.all()  # Get all projects

    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')
        assigned_to = request.form['assigned_to']
        project_id = request.form['project']  # Get the selected project

        # Create a new task and add it to the database
        new_task = Task(title=title, description=description, assigned_to=assigned_to, created_by=current_user.id, project_id=project_id)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('main.dashboard'))  # Redirect after submission

    return render_template('add_task.html', users=users, projects=projects)

# delete task route
@main.route("/delete_task/<int:task_id>")
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route("/add_project", methods=['GET', 'POST'])
@login_required
def add_project():
    if current_user.role != 'admin':
        flash('You do not have permission to add projects.', 'danger')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        # Validate input
        if not title or not description:
            flash('Title and description are required.', 'danger')
            return redirect(url_for('main.add_project'))

        # Create a new project
        project = Project(title=title, description=description, created_by=current_user.id)  # Assign creator
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('add_project.html')

@main.route("/edit_project/<int:project_id>", methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if current_user.role != 'admin':
        flash('You do not have permission to edit projects.', 'danger')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('edit_project.html', project=project)

@main.route("/delete_project/<int:project_id>")
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    if current_user.role != 'admin':
        flash('You do not have permission to delete projects.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route("/view_project/<int:project_id>")
@login_required
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project.id).all()
    return render_template('view_project.html', project=project, tasks=tasks)
