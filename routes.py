from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User, Skill, Interlist, College
from functools import wraps
from datetime import datetime, timedelta
import json
import os
from werkzeug.utils import secure_filename
from flask import current_app
from otp_utils import generate_otp, verify_otp
from sqlalchemy import distinct
import google.generativeai as genai

# Set your Gemini API key
GEMINI_API_KEY = "AIzaSyDLcc-3qGihQ1EfwcPeB9KUJTaWelsASvk"

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)
user = Blueprint('user', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

# Main routes
@main.route('/')
def home():
    return render_template('home.html')

@main.route('/discover-skills')
def discover_skills():
    return render_template('discover_skills.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/skills/web-development')
def web_development():
    return render_template('skills/webdevelopment.html')

@main.route('/skills/data-science')
def data_science():
    return render_template('skills/datascience.html')

@main.route('/skills/ux-ui-design')
def ux_ui_design():
    return render_template('skills/uxuidesign.html')

@main.route('/skills/digital-marketing')
def digital_marketing():
    return render_template('skills/digitalmarketing.html')

@main.route('/skills/mobile-app-development')
def mobile_app_development():
    return render_template('skills/mobileappdevelopment.html')

@main.route('/skills/cloud-computing')
def cloud_computing():
    return render_template('skills/cloudcomputing.html')

@main.route('/careers')
def careers():
    return render_template('careers.html')

@main.route('/career-suggestion')
def career_suggestion():
    return render_template('career_suggestion.html')

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    # Calculate profile completion percentage
    profile_fields = [
        current_user.full_name,
        current_user.email,
        current_user.bio,
        current_user.profile_picture
    ]
    completed_fields = sum(1 for field in profile_fields if field)
    profile_completion = int((completed_fields / len(profile_fields)) * 100)
    
    # Get recent activities (you can implement this based on your needs)
    recent_activities = []
    
    # Get recommended skills (you can implement this based on your needs)
    recommended_skills = []
    
    return render_template('user/dashboard.html',
                         profile_completion=profile_completion,
                         recent_activities=recent_activities,
                         recommended_skills=recommended_skills)

@main.route('/terms')
def terms():  
    return render_template('terms.html')

@main.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html')

@main.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    user = current_user
    
    # Update profile information
    user.full_name = request.form.get('full_name')
    user.email = request.form.get('email')
    user.bio = request.form.get('bio')
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('main.profile'))

@main.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not check_password_hash(current_user.password_hash, current_password):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('main.profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('main.profile'))
    
    current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    flash('Password changed successfully!', 'success')
    return redirect(url_for('main.profile'))

@main.route('/profile/update-photo', methods=['POST'])
@login_required
def update_photo():
    if 'photo' not in request.files:
        flash('No file selected.', 'danger')
        return redirect(url_for('main.profile'))
    
    file = request.files['photo']
    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('main.profile'))
    
    if file and allowed_file(file.filename):
        try:
            # Generate a unique filename
            filename = secure_filename(f"{current_user.id}_{file.filename}")
            
            # Save the file
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Delete old profile picture if it exists
            if current_user.profile_picture:
                old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.profile_picture)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            # Update user's profile picture
            current_user.profile_picture = filename
            db.session.commit()
            
            flash('Profile photo updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating profile photo: {str(e)}', 'danger')
    else:
        flash('Invalid file type. Please upload a PNG, JPG, JPEG, or GIF file.', 'danger')
    
    return redirect(url_for('main.profile'))

# Auth routes
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        print(f"Login attempt - Username/Email: {username_or_email}")  # Debug log
        
        # Try to find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | 
            (User.email == username_or_email)
        ).first()
        
        if not user:
            print(f"User not found: {username_or_email}")  # Debug log
            flash('Invalid username/email or password.', 'error')
            return redirect(url_for('auth.login'))
            
        if user.check_password(password):
            print(f"Password check successful for user: {user.username}")  # Debug log
            
            if not user.phone_number:
                print(f"No phone number found for user: {user.username}")  # Debug log
                flash('Phone number not found. Please update your profile.', 'error')
                return redirect(url_for('auth.login'))
            
            try:
                # Print Twilio configuration
                print("Twilio Configuration:")
                print(f"Account SID: {current_app.config['TWILIO_ACCOUNT_SID']}")
                print(f"Auth Token: {'*' * len(current_app.config['TWILIO_AUTH_TOKEN']) if current_app.config['TWILIO_AUTH_TOKEN'] else 'Not set'}")
                print(f"Verify SID: {current_app.config['TWILIO_VERIFY_SID']}")
                
                # Generate and send verification code
                verification_sid = generate_otp(user.phone_number)
                print(f"Verification SID: {verification_sid}")  # Debug log
                
                if verification_sid is None:
                    print("Failed to generate verification code")  # Debug log
                    flash('Failed to generate verification code. Please try again.', 'error')
                    return redirect(url_for('auth.login'))
                
                # Store user info in session for OTP verification
                session['pending_user_id'] = user.id
                session['remember'] = bool(remember)
                print(f"Verification code sent successfully to {user.phone_number}")  # Debug log
                flash('Verification code has been sent to your phone number.', 'success')
                return redirect(url_for('auth.verify_login_otp'))
            except Exception as e:
                print(f"Error during verification process: {str(e)}")  # Debug log
                flash('An error occurred while sending verification code. Please try again.', 'error')
                return redirect(url_for('auth.login'))
        else:
            print(f"Password check failed for user: {user.username}")  # Debug log
            flash('Invalid username/email or password.', 'error')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@auth.route('/verify-login-otp', methods=['GET', 'POST'])
def verify_login_otp():
    if 'pending_user_id' not in session:
        print("No pending user found in session")  # Debug log
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        otp = request.form.get('otp')
        user = User.query.get(session['pending_user_id'])
        
        if not user:
            print(f"User not found for pending_user_id: {session['pending_user_id']}")  # Debug log
            session.pop('pending_user_id', None)
            session.pop('remember', None)
            flash('Session expired. Please login again.', 'error')
            return redirect(url_for('auth.login'))
        
        try:
            if verify_otp(user.phone_number, otp):
                print(f"OTP verified successfully for user: {user.username}")  # Debug log
                # Clear session data
                pending_user_id = session.pop('pending_user_id', None)
                remember = session.pop('remember', False)
                
                # Log in the user
                login_user(user, remember=remember)
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                flash('Login successful!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                print(f"Invalid OTP for user: {user.username}")  # Debug log
                flash('Invalid or expired OTP. Please try again.', 'error')
        except Exception as e:
            print(f"Error during OTP verification: {str(e)}")  # Debug log
            flash('An error occurred while verifying OTP. Please try again.', 'error')
    
    return render_template('verify_login_otp.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        education = request.form.get('education')
        
        # Format phone number to E.164 format
        if phone_number:
            # Remove any spaces, dashes, or parentheses
            phone_number = ''.join(filter(str.isdigit, phone_number))
            # Add +1 if it's a US number without country code
            if len(phone_number) == 10:
                phone_number = '+1' + phone_number
            elif not phone_number.startswith('+'):
                phone_number = '+' + phone_number
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('auth.signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return redirect(url_for('auth.signup'))
            
        if User.query.filter_by(phone_number=phone_number).first():
            flash('Phone number already registered.', 'error')
            return redirect(url_for('auth.signup'))
        
        # Set role to 'admin' if it's the first user, otherwise 'user'
        role = 'admin' if User.query.count() == 0 else 'user'
        
        new_user = User(
            username=username,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            role=role,
            education=education
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # TODO: Implement password reset email functionality
            flash('Password reset instructions have been sent to your email.', 'info')
        else:
            flash('No account found with that email address.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')

@auth.route('/google-login')
def google_login():
    # TODO: Implement Google OAuth login
    flash('Google login not implemented yet.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/facebook-login')
def facebook_login():
    # TODO: Implement Facebook OAuth login
    flash('Facebook login not implemented yet.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/twitter-login')
def twitter_login():
    # TODO: Implement Twitter OAuth login
    flash('Twitter login not implemented yet.', 'info')
    return redirect(url_for('auth.login'))

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_skills = Skill.query.count()
    active_users = User.query.filter(User.last_login >= datetime.utcnow() - timedelta(days=7)).count()
    recent_activities = []  # You can implement activity tracking later
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_skills=total_skills,
                         active_users=active_users,
                         recent_activities=recent_activities)

@admin.route('/manage_users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin.route('/manage_skills')
@login_required
@admin_required
def manage_skills():
    skills = Skill.query.all()
    return render_template('admin/manage_skills.html', skills=skills)

@admin.route('/add_college', methods=['POST'])
@login_required
@admin_required
def add_college():
    college_name = request.form.get('college_name')
    college_location = request.form.get('college_location')
    college_website = request.form.get('college_website')
    
    new_college = College(name=college_name, location=college_location, website=college_website)
    db.session.add(new_college)
    db.session.commit()
    
    flash('College added successfully!', 'success')
    return redirect(url_for('admin.manage_colleges'))

@user.route('/search-colleges')
@login_required
def user_search_colleges():
    # Get filter parameters
    state = request.args.get('state', '')
    district = request.args.get('district', '')
    stream = request.args.get('stream', '')
    college_type = request.args.get('college_type', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Base query
    query = Interlist.query

    # Apply filters
    if state:
        query = query.filter(Interlist.State_name == state)
    if district:
        query = query.filter(Interlist.District_Name == district)
    if stream:
        query = query.filter(Interlist.Stream == stream)
    if college_type:
        query = query.filter(Interlist.College_Nature_Type == college_type)

    # Get unique values for filters
    states = db.session.query(distinct(Interlist.State_name)).order_by(Interlist.State_name).all()
    states = [state[0] for state in states if state[0]]

    districts = []
    if state:
        districts = db.session.query(distinct(Interlist.District_Name))\
            .filter(Interlist.State_name == state)\
            .order_by(Interlist.District_Name).all()
        districts = [district[0] for district in districts if district[0]]

    streams = db.session.query(distinct(Interlist.Stream)).order_by(Interlist.Stream).all()
    streams = [stream[0] for stream in streams if stream[0]]

    college_types = db.session.query(distinct(Interlist.College_Nature_Type))\
        .order_by(Interlist.College_Nature_Type).all()
    college_types = [type[0] for type in college_types if type[0]]

    # Paginate results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    colleges = pagination.items

    return render_template('user/college_search.html',
                         colleges=colleges,
                         pagination=pagination,
                         states=states,
                         districts=districts,
                         streams=streams,
                         college_types=college_types,
                         selected_state=state,
                         selected_district=district,
                         selected_stream=stream,
                         selected_type=college_type)

@user.route('/api/districts/<state>')
@login_required
def get_districts(state):
    districts = db.session.query(distinct(Interlist.District_Name))\
        .filter(Interlist.State_name == state)\
        .order_by(Interlist.District_Name).all()
    return jsonify([district[0] for district in districts if district[0]])

@user.route('/discover-skills')
@login_required
def user_discover_skills():
    return render_template('user/discover_skills.html')

@user.route('/settings')
@login_required
def settings():
    return render_template('user/settings.html', settings=current_user)

@user.route('/update-phone', methods=['POST'])
@login_required
def update_phone():
    phone_number = request.form.get('phone_number')
    
    # Format phone number to E.164 format
    if phone_number:
        # Remove any spaces, dashes, or parentheses
        phone_number = ''.join(filter(str.isdigit, phone_number))
        # Add +1 if it's a US number without country code
        if len(phone_number) == 10:
            phone_number = '+1' + phone_number
        elif not phone_number.startswith('+'):
            phone_number = '+' + phone_number
    
    current_user.phone_number = phone_number
    db.session.commit()
    
    flash('Phone number updated successfully!', 'success')
    return redirect(url_for('user.settings'))

@user.route('/settings/delete-account', methods=['POST'])
@login_required
def delete_account():
    password = request.form.get('password')
    
    if not check_password_hash(current_user.password_hash, password):
        flash('Incorrect password. Please try again.', 'danger')
        return redirect(url_for('user.settings'))
    
    # Delete user's skills first
    Skill.query.filter_by(user_id=current_user.id).delete()
    
    # Delete the user
    db.session.delete(current_user)
    db.session.commit()
    
    logout_user()
    flash('Your account has been deleted successfully.', 'success')
    return redirect(url_for('auth.login'))

@user.route('/settings/export-data')
@login_required
def export_data():
    user_data = {
        'username': current_user.username,
        'email': current_user.email,
        'full_name': current_user.full_name,
        'bio': current_user.bio,
        'created_at': current_user.created_at.isoformat(),
        'last_login': current_user.last_login.isoformat() if current_user.last_login else None,
        'skills': [
            {
                'name': skill.name,
                'level': skill.level,
                'experience_years': skill.experience_years,
                'created_at': skill.created_at.isoformat(),
                'updated_at': skill.updated_at.isoformat()
            }
            for skill in current_user.skills
        ]
    }
    
    response = jsonify(user_data)
    response.headers['Content-Disposition'] = f'attachment; filename=user_data_{current_user.username}.json'
    return response

@user.route('/skills')
@login_required
def skills():
    user_skills = current_user.skills
    return render_template('user/skills.html', user_skills=user_skills)

@user.route('/skills/add', methods=['POST'])
@login_required
def add_skill():
    name = request.form.get('name')
    level = int(request.form.get('level'))
    experience = float(request.form.get('experience'))
    
    skill = Skill(
        name=name,
        level=level,
        experience_years=experience,
        user_id=current_user.id
    )
    
    db.session.add(skill)
    db.session.commit()
    
    flash('Skill added successfully!', 'success')
    return redirect(url_for('user.skills'))

@user.route('/skills/edit', methods=['POST'])
@login_required
def edit_skill():
    skill_id = request.form.get('skill_id')
    skill = Skill.query.get_or_404(skill_id)
    
    if skill.user_id != current_user.id:
        flash('You do not have permission to edit this skill.', 'danger')
        return redirect(url_for('user.skills'))
    
    skill.name = request.form.get('name')
    skill.level = int(request.form.get('level'))
    skill.experience_years = float(request.form.get('experience'))
    
    db.session.commit()
    flash('Skill updated successfully!', 'success')
    return redirect(url_for('user.skills'))

@user.route('/skills/delete', methods=['POST'])
@login_required
def delete_skill():
    skill_id = request.form.get('skill_id')
    skill = Skill.query.get_or_404(skill_id)
    
    if skill.user_id != current_user.id:
        flash('You do not have permission to delete this skill.', 'danger')
        return redirect(url_for('user.skills'))
    
    db.session.delete(skill)
    db.session.commit()
    
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('user.skills'))

# Helper function for file uploads
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/otp-verification', methods=['GET', 'POST'])
def otp_verification():
    if request.method == 'POST':
        phone = request.form.get('phone')
        otp = request.form.get('otp')
        
        if verify_otp(phone, otp):
            flash('Phone number verified successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid or expired OTP. Please try again.', 'danger')
    
    return render_template('otp_verification.html')

@auth.route('/send-otp', methods=['POST'])
def send_otp():
    phone = request.form.get('phone')
    if not phone:
        return jsonify({'success': False, 'message': 'Phone number is required'})
    
    verification_sid = generate_otp(phone)
    if verification_sid:
        return jsonify({'success': True, 'message': 'Verification code sent successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to send verification code'})

@auth.route('/resend-otp', methods=['POST'])
def resend_otp():
    data = request.get_json()
    phone = data.get('phone')
    
    if not phone:
        return jsonify({'success': False, 'message': 'Phone number is required'})
    
    verification_sid = generate_otp(phone)
    if verification_sid:
        return jsonify({'success': True, 'message': 'Verification code resent successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to resend verification code'})

@user.route('/ai-chatbot')
@login_required
def ai_chatbot():
    return render_template('user/ai_chatbot.html')

@user.route('/ai-chatbot/chat', methods=['POST'])
@login_required
def ai_chat():
    try:
        # Initialize Gemini here
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        data = request.get_json()
        user_message = data.get('message', '').lower()
        session_data = session.get('chat_data', {})

        if not user_message:
            return jsonify({'response': "Please enter a message.", 'is_multi_response': False})

        # Initialize chat flow if not started
        if 'step' not in session_data:
            session_data['step'] = 'name'
            session_data['name'] = user_message
            session['chat_data'] = session_data
            return jsonify({
                'response': f"Nice to meet you, {user_message}! What is your highest level of education?\n\nPlease choose one:\n- Below 10th\n- Completed 10th\n- Intermediate\n- Diploma\n- B.Tech\n- B.Com\n- Other",
                'is_multi_response': False
            })

        # Handle education level
        if session_data['step'] == 'name':
            session_data['step'] = 'education'
            session_data['education'] = user_message
            session['chat_data'] = session_data

            if 'below 10th' in user_message or 'completed 10th' in user_message:
                return jsonify({
                    'response': "Which subjects interest you the most?\n\nPlease mention your top 3 interests from:\n- Mathematics\n- Physics\n- Chemistry\n- Biology\n- Computer Science\n- Commerce\n- Arts\n- Other",
                    'is_multi_response': False
                })
            elif 'intermediate' in user_message:
                return jsonify({
                    'response': "Great! What stream did you choose in intermediate?\n\nPlease select:\n- Science (PCM)\n- Science (PCB)\n- Commerce\n- Arts",
                    'is_multi_response': False
                })
            elif 'diploma' in user_message:
                return jsonify({
                    'response': "Which field did you specialize in during your diploma?\n\nPlease mention your specialization.",
                    'is_multi_response': False
                })
            elif 'btech' in user_message:
                return jsonify({
                    'response': "Which branch did you study in B.Tech?\n\nPlease mention your specialization.",
                    'is_multi_response': False
                })
            elif 'bcom' in user_message:
                return jsonify({
                    'response': "What are your career interests after B.Com?\n\nPlease choose:\n- Finance\n- Marketing\n- Human Resources\n- Entrepreneurship\n- Other",
                    'is_multi_response': False
                })
            else:
                return jsonify({
                    'response': "Please tell me more about your educational background and interests.",
                    'is_multi_response': False
                })

        # Handle subject interests for 10th or below
        elif session_data['step'] == 'education' and ('below 10th' in session_data['education'] or 'completed 10th' in session_data['education']):
            session_data['step'] = 'subjects'
            session_data['subjects'] = user_message
            session['chat_data'] = session_data

            # Create a structured prompt for career guidance
            prompt = f"""As a career guidance AI assistant, provide specific career path recommendations based on the following information:

Education Level: {session_data['education']}
Subject Interests: {user_message}

Guidelines:
- Suggest 2-3 specific career paths
- Include required qualifications
- List key skills needed
- Provide immediate next steps
- Keep response under 100 words
- Focus on practical, achievable goals"""

            response = model.generate_content(prompt)
            return jsonify({
                'response': response.text,
                'is_multi_response': False
            })

        # Handle other education levels
        else:
            # Create a structured prompt for career guidance
            prompt = f"""As a career guidance AI assistant, provide specific career path recommendations based on the following information:

Education Level: {session_data['education']}
Current Response: {user_message}

Guidelines:
- Suggest 2-3 specific career paths
- Include required qualifications
- List key skills needed
- Provide immediate next steps
- Keep response under 100 words
- Focus on practical, achievable goals"""

            response = model.generate_content(prompt)
            return jsonify({
                'response': response.text,
                'is_multi_response': False
            })

    except Exception as e:
        print(f"Chat error: {str(e)}")  # Debug print
        return jsonify({
            'response': "Sorry, there was an error processing your request. Please try again.",
            'is_multi_response': False
        }), 500 