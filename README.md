`pip install flask flask_sqlalchemy`

```
job_tracker/
├── app.py                ← main Flask app
├── models.py             ← defines the Job model (database table)
├── templates/            ← HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add.html
│   └── jobs.html
└── instance/
    └──  job_tracker.db        ← (auto-created SQLite database)
```
