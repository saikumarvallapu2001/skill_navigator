from extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    full_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    profile_picture = db.Column(db.String(200))
    education = db.Column(db.String(50))  # New education field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    phone_number = db.Column(db.String(20), unique=True)
    
    # Settings
    email_updates = db.Column(db.Boolean, default=True)
    email_newsletter = db.Column(db.Boolean, default=True)
    email_marketing = db.Column(db.Boolean, default=False)
    skill_recommendations = db.Column(db.Boolean, default=True)
    career_suggestions = db.Column(db.Boolean, default=True)
    profile_visibility = db.Column(db.Boolean, default=True)
    show_skills = db.Column(db.Boolean, default=True)
    
    # Relationships
    skills = db.relationship('Skill', backref='user', lazy=True)
    
    # Education choices
    EDUCATION_CHOICES = [
        ('school', 'School'),
        ('intermediate', 'Intermediate'),
        ('polytechnic', 'Polytechnic'),
        ('bachelors', 'Bachelors'),
        ('masters', 'Masters'),
        ('phd', 'PhD'),
        ('other', 'Other')
    ]
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer)  # 1-5 scale
    experience_years = db.Column(db.Float)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Skill {self.name}>'

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # e.g., 'skill_added', 'profile_updated'
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='activities')

class Interlist(db.Model):
    __tablename__ = 'interlist'
    
    S_NO = db.Column(db.Integer, primary_key=True)
    College_Name = db.Column(db.String(75))
    State_name = db.Column(db.String(13))
    District_Name = db.Column(db.String(27))
    College_Address = db.Column(db.String(238))
    College_Nature_Type = db.Column(db.String(27))
    Stream = db.Column(db.String(18))
    Email_Id = db.Column(db.String(43))

    def __repr__(self):
        return f'<College {self.College_Name}>'

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)