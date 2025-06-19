from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('skills/web-development/', views.web_development, name='web_development'),
    path('skills/data-science/', views.data_science, name='data_science'),
    path('skills/ux-ui-design/', views.ux_ui_design, name='ux_ui_design'),
    path('skills/digital-marketing/', views.digital_marketing, name='digital_marketing'),
    path('skills/mobile-app-development/', views.mobile_app_development, name='mobile_app_development'),
    path('skills/cloud-computing/', views.cloud_computing, name='cloud_computing'),
    path('careers/', views.careers, name='careers'),
    path('career-suggestion/', views.career_suggestion, name='career_suggestion'),
] 