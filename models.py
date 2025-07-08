from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    date_applied = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Job {self.title} at {self.company}>"
