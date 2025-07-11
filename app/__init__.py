import os
from flask import Flask
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from app.models import db, User
from app.routes.auth import auth_bp
from app.routes.job_routes import job_bp
from app.routes.home import home_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    os.makedirs("instance", exist_ok=True)
    app.config.from_pyfile("../config.py")

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    JWTManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(job_bp)

    with app.app_context():
        db.create_all()

    return app
