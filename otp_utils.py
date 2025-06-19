import os
from datetime import datetime, timedelta
from twilio.rest import Client
from flask import current_app
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store OTPs temporarily (in production, use Redis or a database)
otp_store = {}

def generate_otp(phone):
    """Generate and send OTP using Twilio Verify"""
    try:
        # Get Twilio credentials from config
        account_sid = current_app.config['TWILIO_ACCOUNT_SID']
        auth_token = current_app.config['TWILIO_AUTH_TOKEN']
        verify_sid = current_app.config['TWILIO_VERIFY_SID']
        
        logger.info(f"Attempting to send verification code to {phone}")
        
        if not all([account_sid, auth_token, verify_sid]):
            logger.error("Twilio credentials not configured")
            logger.error(f"Account SID: {'Present' if account_sid else 'Missing'}")
            logger.error(f"Auth Token: {'Present' if auth_token else 'Missing'}")
            logger.error(f"Verify SID: {'Present' if verify_sid else 'Missing'}")
            return None
        
        client = Client(account_sid, auth_token)
        
        # Send verification code
        verification = client.verify.v2.services(verify_sid) \
            .verifications \
            .create(to=phone, channel='sms')
        
        logger.info(f"Verification sent successfully to {phone}")
        logger.info(f"Verification SID: {verification.sid}")
        return verification.sid
    except Exception as e:
        logger.error(f"Error sending verification code: {str(e)}")
        return None

def verify_otp(phone, otp):
    """Verify the OTP using Twilio Verify"""
    try:
        # Get Twilio credentials from config
        account_sid = current_app.config['TWILIO_ACCOUNT_SID']
        auth_token = current_app.config['TWILIO_AUTH_TOKEN']
        verify_sid = current_app.config['TWILIO_VERIFY_SID']
        
        logger.info(f"Attempting to verify code for {phone}")
        
        if not all([account_sid, auth_token, verify_sid]):
            logger.error("Twilio credentials not configured")
            return False
        
        client = Client(account_sid, auth_token)
        
        # Check verification
        verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=phone, code=otp)
        
        logger.info(f"Verification status: {verification_check.status}")
        return verification_check.status == 'approved'
    except Exception as e:
        logger.error(f"Error verifying code: {str(e)}")
        return False 