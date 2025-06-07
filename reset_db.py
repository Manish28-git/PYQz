from app import create_app, db

app = create_app()

with app.app_context():
    db.drop_all()    # Delete all existing tables
    db.create_all()  # Recreate all tables from updated models
    print("✅ Database reset and created again.")
