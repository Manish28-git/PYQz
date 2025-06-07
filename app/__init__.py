import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = 'your-secret-key'
    basedir = os.path.abspath(os.path.dirname(__file__))
    # SQLite DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'papers.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Uploads folder
    upload_folder = os.path.join(basedir, '..', 'uploads')
    app.config['UPLOAD_FOLDER'] = upload_folder
    os.makedirs(upload_folder, exist_ok=True)

    db.init_app(app)

    # Import models
    from .models import Paper
    from .routes import main
    app.register_blueprint(main)

    # Create tables & year folders
    with app.app_context():
        db.create_all()
        for y in range(2018, 2026):
            folder = f"{y-1}-{y}"
            os.makedirs(os.path.join(upload_folder, folder), exist_ok=True)

    return app
