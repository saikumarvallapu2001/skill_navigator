from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User

# Create your views here.

def landing_page(request):
    return render(request, 'core/landing_page.html')

def discover_skills(request):
    return render(request, 'core/discover_skills.html')

def web_development(request):
    return render(request, 'core/skills/webdevelopment.html')

def data_science(request):
    return render(request, 'core/skills/datascience.html')

def ux_ui_design(request):
    return render(request, 'core/skills/uxuidesign.html')

def digital_marketing(request):
    return render(request, 'core/skills/digitalmarketing.html')

def mobile_app_development(request):
    return render(request, 'core/skills/mobileappdevelopment.html')

def cloud_computing(request):
    return render(request, 'core/skills/cloudcomputing.html')

def about(request):
    return render(request, 'core/about.html')

def careers(request):
    return render(request, 'core/careers.html')

def career_suggestion(request):
    return render(request, 'core/career_suggestion.html')

def contact(request):
    return render(request, 'core/contact.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login successful
            login(request, user)
            
            # Set session expiry based on remember me
            if not remember:
                request.session.set_expiry(0)  # Session expires when browser closes
            
            messages.success(request, 'Login successful!')
            return redirect('dashboard')  # Redirect to dashboard or home page
        else:
            # Login failed
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'core/login.html')

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

def signup(request):
    return render(request, 'core/signup.html')

def home(request):
    return render(request, 'core/home.html')




