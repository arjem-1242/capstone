from django.urls import path
from . import views

from .views import *
from django.contrib.auth import views as auth_views

app_name = 'jobseeker'

urlpatterns = [
    path('job_seeker_dashboard/', views.job_seeker_dashboard, name="jobseeker_dashboard"),

    path('about/', views.jobseeker_about, name="jobseeker_about"),
    path('services/', views.jobseeker_services, name="jobseeker_services"),
    path('contact/', views.jobseeker_contact, name="jobseeker_contact"),
    path('services/1', views.jobseeker_service_detail_1, name="jobseeker_service_detail_1"),
    path('services/2', views.jobseeker_service_detail_2, name="jobseeker_service_detail_2"),
    path('services/3', views.jobseeker_service_detail_3, name="jobseeker_service_detail_3"),
    path('services/4', views.jobseeker_service_detail_4, name="jobseeker_service_detail_4"),
    path('services/5', views.jobseeker_service_detail_5, name="jobseeker_service_detail_5"),
    path('services/6', views.jobseeker_service_detail_6, name="jobseeker_service_detail_6"),
    path('faqs/', views.jobseeker_faqs, name="jobseeker_faqs"),

    # Jobseeker Profile
    path('job_seeker/profile/', views.job_seeker_profile, name="job_seeker_profile"),
    path('change-password/', views.jobseeker_change_password, name='jobseeker_change_password'),
    path('job_seeker/upload_resume/', views.upload_resume, name="upload_resume"),
    path('job_seeker/update_profile/', views.update_profile_bulk, name="update_profile_bulk"),
    path("update-profile-field/", update_profile_field, name="update_profile_field"),
    path('matched_jobs/', views.view_matched_jobs, name='view_matched_jobs'),
    path("add-education/", add_education, name="add-education"),
    path("update-education/<int:education_id>/", update_education, name="update-education"),
    path('delete-education/<int:education_id>/', views.delete_education, name='delete-education'),
    path('add-employment/', views.add_employment, name='add-employment'),
    path('update-employment/<int:employment_id>/', views.update_employment, name='update-employment'),
    path('delete-employment/<int:employment_id>/', views.delete_employment, name='delete-employment'),
    path('job_seeker/delete_profile/', views.delete_profile, name="delete_profile"),

    ]