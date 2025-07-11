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
├── app/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── home.py
│   │   └── job_routes.py
│   ├── templates/
│   │   ├── add.html
│   │   ├── base.html
│   │   ├── edit.html
│   │   ├── index.html
│   │   ├── jobs.html
│   │   ├── login.html
│   │   └── register.html
│   └── __init__.py
├── instance/
├── migrations/
├── .gitignore
├── config.py
├── README.md
└── run.py

```
