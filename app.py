from flask import Flask, render_template, request, redirect, url_for
from models import db, Job

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        date_applied = request.form['date_applied']

        new_job = Job(title=title, company=company, date_applied=date_applied)
        db.session.add(new_job)
        db.session.commit()

        return redirect(url_for('view_jobs'))
    return render_template('add.html')

@app.route('/jobs')
def view_jobs():
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
