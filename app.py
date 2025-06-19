from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from config import Config
from extensions import db, login_manager
from models import User
from routes import main, auth, admin, user
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from flask_session import Session
import secrets
import string
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import re
import google.generativeai as genai

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    Session(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Set up user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(user, url_prefix='/user')

    # Configure logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/skill_navigator.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Skill Navigator startup')

    return app

# Create the application instance
app = create_app()

@app.route('/career-suggestion', methods=['GET', 'POST'])
def career_suggestion():
    if request.method == 'POST':
        # Collect form data
        name = request.form.get('name')
        email = request.form.get('email')
        marks = request.form.get('marks')
        education = request.form.get('education')
        stream = request.form.get('stream')
        caste = request.form.get('caste')
        state = request.form.get('state')
        city = request.form.get('city')

        # Prepare prompt for Gemini
        prompt = (
            f"Suggest a single word (career title) for a person with the following details:\n"
            f"Name: {name}\n"
            f"Education: {education}\n"
            f"Stream: {stream}\n"
            f"Marks: {marks}\n"
            f"Caste: {caste}\n"
            f"State: {state}\n"
            f"City: {city}\n"
            f"Only reply with the one word."
        )

        # Call Gemini
        genai.configure(api_key="AIzaSyDLcc-3qGihQ1EfwcPeB9KUJTaWelsASvk")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        career = response.text.strip().split()[0]  # Get the first word

        return jsonify({'career': career})

    return render_template('career_suggestion.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 