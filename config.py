import os
from dotenv import load_dotenv
from datetime import timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to the project root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file
env_path = os.path.join(BASE_DIR, '.env')
logger.info(f"Looking for .env file at: {env_path}")
load_dotenv(env_path)

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    
    # Session settings
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_FILE_DIR = os.path.join(BASE_DIR, 'flask_session_data')
    
    # Database settings
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'skill_navigator')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Create upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        
    # Twilio settings (hardcoded for local/dev use)
    TWILIO_ACCOUNT_SID = 'ACac40654bde044bee3f9fcca4d0bdeed5'
    TWILIO_AUTH_TOKEN = 'dfb1d78bf157398722652f362ce20cbd'
    TWILIO_VERIFY_SID = 'VA97670d71a71ccd367fe6d87964a90252'  # Replace with your actual Verify SID if needed
    
    # Log Twilio configuration
    logger.info("Loading Twilio configuration...")
    logger.info(f"TWILIO_ACCOUNT_SID: {TWILIO_ACCOUNT_SID}")
    logger.info(f"TWILIO_AUTH_TOKEN: {'*' * len(TWILIO_AUTH_TOKEN) if TWILIO_AUTH_TOKEN else 'Not set'}")
    logger.info(f"TWILIO_VERIFY_SID: {TWILIO_VERIFY_SID}")
    
    # OTP configuration
    OTP_EXPIRY_MINUTES = 5
    OTP_LENGTH = 6 
