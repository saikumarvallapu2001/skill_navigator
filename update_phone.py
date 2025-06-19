from flask import Flask
from extensions import db
from models import User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def update_phone():
    with app.app_context():
        # Find your user
        user = User.query.filter_by(email='sai.19914422@gmail.com').first()
        if user:
            # Force update to Indian format
            phone = '6301516308'  # Your original number without country code
            phone = '+91' + phone  # Add Indian country code
            
            print(f"Updating phone number: {user.phone_number} -> {phone}")
            user.phone_number = phone
            db.session.commit()
            print("Phone number updated successfully!")
        else:
            print("User not found!")

if __name__ == '__main__':
    update_phone() 