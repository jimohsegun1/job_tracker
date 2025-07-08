import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Job
# from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # In production, move this to .env

# === Ensure instance folder exists ===
os.makedirs("instance", exist_ok=True)

# === Absolute DB path ===
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'job_tracker.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# === Initialize DB and Flask-Login ===
db.init_app(app)

# migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirects to login page if @login_required fails

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# === Create DB tables if not exist ===
with app.app_context():
    db.create_all()

# === Routes ===
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("Username already exists!")
            return redirect(url_for('register'))

        # hashed_pw = generate_password_hash(password, method='sha256')
        hashed_pw = generate_password_hash(password)  # uses default method: 'pbkdf2:sha256'
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password")
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('view_jobs'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        date_applied = request.form['date_applied']

        new_job = Job(title=title, company=company, date_applied=date_applied, user_id=current_user.id)
        db.session.add(new_job)
        db.session.commit()

        return redirect(url_for('view_jobs'))
    return render_template('add.html')

@app.route('/jobs')
@login_required
def view_jobs():
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    return render_template('jobs.html', jobs=jobs)


@app.route('/edit/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)

    if job.user_id != current_user.id:
        flash("You don't have permission to edit this job.")
        return redirect(url_for('view_jobs'))

    if request.method == 'POST':
        job.title = request.form['title']
        job.company = request.form['company']
        job.date_applied = request.form['date_applied']
        db.session.commit()
        flash("Job updated successfully.")
        return redirect(url_for('view_jobs'))

    return render_template('edit.html', job=job)

@app.route('/delete/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)

    if job.user_id != current_user.id:
        flash("You don't have permission to delete this job.")
        return redirect(url_for('view_jobs'))

    db.session.delete(job)
    db.session.commit()
    flash("Job deleted successfully.")
    return redirect(url_for('view_jobs'))


if __name__ == '__main__':
    app.run(debug=True)
