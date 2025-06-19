from flask import Flask
from flask_migrate import Migrate, upgrade
from app import app, db
from extensions import db as ext_db
from models import User, Skill
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app import create_app

def migrate_database():
    app = app
    with app.app_context():
        # Drop existing tables
        ext_db.drop_all()
        
        # Create tables with new schema
        ext_db.create_all()
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash='scrypt:32768:8:1$Dw85iGzGWfbIfTuM$c08a643fea28a87673f8e7811d1e8813de7f24e6b60434f355c08586bdfe6905e4a3cbf9d967a14be94e425156ec9aa2aa99a453bcfa7768eee3627a96eba137',
            role='admin',
            full_name='Admin User',
            email_updates=True,
            email_newsletter=True,
            email_marketing=False,
            skill_recommendations=True,
            career_suggestions=True,
            profile_visibility=True,
            show_skills=True
        )
        
        # Create regular user
        user = User(
            username='user',
            email='user@example.com',
            password_hash='scrypt:32768:8:1$z67tSQr1jZZulep3$718245186fe8e4b4cdeda6b704f957535fdf5ff79898ecc01ccbc2468d299acebd7ed7a388f8a996011fbb6e5b7f7864b77c7f5059e7b5d0d12f7a2472004478',
            role='user',
            full_name='Regular User',
            email_updates=True,
            email_newsletter=True,
            email_marketing=False,
            skill_recommendations=True,
            career_suggestions=True,
            profile_visibility=True,
            show_skills=True
        )
        
        # Add users to database
        ext_db.session.add(admin)
        ext_db.session.add(user)
        ext_db.session.commit()
        
        print("Database migration completed successfully!")

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Run any pending migrations
        migrate = Migrate(app, db)
        upgrade()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    return app, db

def upgrade():
    app, db = create_app()
    with app.app_context():
        try:
            db.engine.execute('ALTER TABLE users ADD COLUMN phone_number VARCHAR(20) UNIQUE')
        except Exception as e:
            print(f'Column may already exist or another error occurred: {e}')
        # Optionally, make phone_number NOT NULL if you want to enforce it for all users
        # db.engine.execute('ALTER TABLE users MODIFY COLUMN phone_number VARCHAR(20) UNIQUE NOT NULL')

def downgrade():
    app, db = create_app()
    with app.app_context():
        # Remove phone_number column from User table
        db.engine.execute('ALTER TABLE user DROP COLUMN phone_number')

def format_phone_number(phone):
    if not phone:
        return None
    # Remove any spaces, dashes, or parentheses
    phone = ''.join(filter(str.isdigit, phone))
    # Add +1 if it's a US number without country code
    if len(phone) == 10:
        phone = '+91' + phone
    elif not phone.startswith('+'):
        phone = '+' + phone
    return phone

def update_phone_numbers():
    app = create_app()
    with app.app_context():
        users = User.query.all()
        for user in users:
            if user.phone_number:
                formatted_phone = format_phone_number(user.phone_number)
                print(f"Updating phone number for {user.username}: {user.phone_number} -> {formatted_phone}")
                user.phone_number = formatted_phone
        db.session.commit()
        print("Phone numbers updated successfully!")

if __name__ == '__main__':
    update_phone_numbers()
    print("Database migration completed successfully!") 