from django.urls import path
from . import views

from .views import *
from django.contrib.auth import views as auth_views

app_name = 'employer'

urlpatterns = [
    path('employer-dashboard/', views.employer_dashboard, name="employer_dashboard"),
    path('about/', views.employer_about, name="employer_about"),
    path('services/', views.employer_services, name="employer_services"),
    path('contact/', views.employer_contact, name="employer_contact"),
    path('services/1', views.employer_service_detail_1, name="employer_service_detail_1"),
    path('services/2', views.employer_service_detail_2, name="employer_service_detail_2"),
    path('services/3', views.employer_service_detail_3, name="employer_service_detail_3"),
    path('services/4', views.employer_service_detail_4, name="employer_service_detail_4"),
    path('services/5', views.employer_service_detail_5, name="employer_service_detail_5"),
    path('services/6', views.employer_service_detail_6, name="employer_service_detail_6"),
    path('job/list', views.job_posting_list, name="job_posting_list"),
    # Company Profile
    path('company/update/<int:pk>/', views.update_company_profile, name='update_company_profile'),
    # Job Posting
    path('job/create/', views.create_job_posting, name='create_job_posting'),
    path('job/update/<int:pk>/', views.update_job_posting, name='update_job_posting'),

    # Accreditation Request
    path('accreditation/create/', views.create_accreditation_request, name='create_accreditation_request'),
    path('accreditation-request-overview/', views.accreditation_request_overview, name='accreditation_request_overview'),

    path('accreditation/load-form-fields/', views.load_accreditation_form_fields, name='load_accreditation_form_fields'),

    path('accreditation/update/<int:pk>/', views.update_accreditation_request, name='update_accreditation_request'),
    # Add this if needed

    # Applicant
    path('applicant/update_resume/', views.update_applicant_resume, name='update_applicant_resume'),
    # path('profile/', views.company_profile_view, name='company_profile_view'),
    path('company-profile/', views.employer_profile_view, name='employer_profile_view'),
    path('change-password/', views.change_password_view, name='change_password_view'),

    # Saved Candidate
    path('job/<int:job_id>/applicant/<int:applicant_id>/save/', views.save_candidate, name='save_candidate'),

    path('faqs/', views.employer_faqs, name="employer_faqs"),
]