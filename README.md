`pip install flask flask_sqlalchemy flask-login flask-wtf`

## ✅ Features:
- User registration (with password hashing)
- Login/logout
- Logged-in users can add/view only their own jobs

## 🔧 Tech stacks:
- Flask-Login: for session management
- Werkzeug.security: for secure password hashing
- Flask-WTF: for form handling (optional — skipping for now to keep it simple)

```
job_tracker/
├── app.py
├── models.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── add.html
│   └── jobs.html
├── instance/
│   └── job_tracker.db

```
