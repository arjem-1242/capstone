from audioop import reverse
from http.client import responses

from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.html import format_html
from core.models import CustomUser

from capstone import settings
from .tokens import generate_token  # Custom token generator
from employer.models import accreditation_document_storage
from jobseeker.models import ResumeDocument, JobseekerProfile, Education, Employment

from employer.models import AccreditationRequest
from .forms import *

app_name = 'core'


# Create your views here.
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'JOB_SEEKER':
            return redirect('job_seeker_dashboard')
        elif request.user.user_type == 'EMPLOYER':
            return redirect('employer_dashboard')
    return render(request, f"{app_name}/home.html")

@never_cache
def dashboard(request):
    return render(request, f"{app_name}/index.html")

@never_cache
def companies(request):
    requests = AccreditationRequest.objects.all()
    return render(request, f"{app_name}/companies.html", {"requests": requests})

@never_cache
def accredited_companies(request):
    return render(request, f"{app_name}/accredited-companies.html")

@never_cache
def jobs(request):
    return render(request, f"{app_name}/jobs.html")

@never_cache
def employees(request):
    return render(request, f"{app_name}/employees.html")

@never_cache
def seminars(request):
    return render(request, f"{app_name}/seminars.html")

@never_cache
def profile(request):
    return render(request, f"{app_name}/users-profile.html")

@never_cache
def job_trends(request):
    return render(request, f"{app_name}/job-trends.html")

@never_cache
def tools(request):
    return render(request, f"{app_name}/tools.html")

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def faqs(request):
    return render(request, f"{app_name}/pages-faq.html")

@never_cache
def analytics(request):
    return render(request, f"{app_name}/analytics.html")

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def job_analytics(request):
    return render(request, f"{app_name}/job-analytics.html")




@never_cache
def login_job_seeker(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'JOB_SEEKER':
            return redirect('job_seeker_dashboard')
        else:
            return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            if not user.is_active:
                return render(request, 'core/login_job_seeker.html', {
                    'error': 'Please verify your email before logging in.'
                })

            if user.user_type == 'JOB_SEEKER':
                login(request, user)
                return redirect('job_seeker_dashboard')
            else:
                return render(request, 'core/login_job_seeker.html', {
                    'error': 'This login is only for job seekers.'
                })

        return render(request, 'core/login_job_seeker.html', {
            'error': 'Please check the entered credentials'
        })

    return render(request, 'core/login_job_seeker.html')
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def logout_job_seeker(request):

    logout(request)
    response = redirect('home')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
def register_job_seeker(request):
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST)

        # Check if email already exists
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            login_url = reverse('login_job_seeker')
            messages.error(
                request,
                format_html(
                    'An account with this email already exists. Please <a href="{}">log in</a> instead.',
                    login_url
                )
            )
            return render(request, 'core/register_job_seeker.html', {'form': form})

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Prevent login until email verification
            user.save()

            # Email confirmation setup
            current_site = get_current_site(request)
            email_subject = "Confirm Your PESO Sync Account"
            email_body = render_to_string('core/email_confirmation.html', {
                'name': user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user),
            })

            email = EmailMessage(email_subject, email_body, settings.EMAIL_HOST_USER, [user.email])
            email.send(fail_silently=True)

            messages.success(request, "Account created! Please check your email to verify your account.")
            return redirect('login_job_seeker')

    else:
        form = JobSeekerRegistrationForm()
        messages.error(request, "Please correct the errors below.")

    return render(request, 'core/register_job_seeker.html', {'form': form})

@login_required
def job_seeker_dashboard(request):
    user = CustomUser.objects.get(pk=request.user.id)
    if request.user.is_authenticated:

        if user.user_type == 'JOB_SEEKER':
            return render(request, 'jobseeker/job_seeker_dashboard.html')
        else:
            return redirect('home')  # Or another appropriate page


@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_peso(request):
    if request.user.is_authenticated:
        return redirect('pesostaff:staff_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if not user.is_active:
                return render(request, 'core/login_peso.html', {'error': 'Please verify your email before logging in.'})
            if user.user_type == 'PESO':
                login(request, user)
                return redirect('pesostaff:staff_dashboard')
            else:
                return render(request, 'core/login_peso.html', {
                    'error': 'This login is only for PESO Staff.'
                })

        return render(request, 'core/login_peso.html', {'error': 'Please check the entered credentials'})

    return render(request, 'core/login_peso.html')

@login_required
@never_cache
def logout_peso(request):

    logout(request)
    return redirect('home')

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_peso(request):
    if request.user.is_authenticated:
        return redirect('pesostaff:staff_dashboard')
    if request.method == 'POST':
        form = PESOStaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Generate email confirmation link
            current_site = get_current_site(request)
            email_subject = "Confirm Your PESO Sync Account"
            email_body = render_to_string('core/peso_email_confirmation.html', {
                'name': user.company_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user),
            })

            print(f"Sending email to: {user.email}")  # ✅ Debugging step
            print(f"Email Subject: {email_subject}")
            print(f"Email Body: {email_body}")
            email = EmailMessage(email_subject, email_body, settings.EMAIL_HOST_USER, [user.email])
            email.send(fail_silently=True)

            messages.success(request, "Account created! Please check your email to verify your account.")
            return redirect('login_peso') # Redirect to login page after registration
    else:
        form = PESOStaffRegistrationForm()
    return render(request, 'core/register_peso.html', {'form': form})

# Forgot password function
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "No account found with that email.")
            return redirect('forgot_password')

        # Generate password reset link
        current_site = get_current_site(request)
        email_subject = "Reset Your Password"
        reset_url = reverse('reset_password', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'user_type': user.user_type.lower()
        })

        email_body = render_to_string('core/password_reset_token.html', {
            'domain': current_site.domain,
            'reset_url': request.build_absolute_uri(reset_url),
        })

        email = EmailMessage(email_subject, email_body, to=[user.email])
        email.send(fail_silently=True)

        messages.success(request, "Password reset link sent! Check your email.")
        return redirect('home')

    return render(request, 'core/password_reset_email.html')

def reset_password(request, uidb64, token, user_type):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'core/reset_password.html', {'user_type': user_type})

            user.set_password(new_password)
            user.save()
            messages.success(request, "Your password has been reset successfully!")
            return redirect(f'login_{user_type.lower()}')

        return render(request, 'core/reset_password.html', {'user_type': user_type})
    else:
        messages.error(request, "The password reset link is invalid or has expired.")
        return redirect('forgot_password')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You may now log in.")
        return redirect('home')  # Change to appropriate login page
    else:
        return render(request, 'core/activation_failed.html')

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def employer_dashboard(request):
    return render(request, 'employer/employer_dashboard.html')

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_employer(request):
    if request.user.is_authenticated:
        return redirect('employer:employer_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if not user.is_active:
                return render(request, 'core/login_employer.html',
                              {'error': 'Please verify your email before logging in.'})
            if user.user_type == 'EMPLOYER':
                login(request, user)
                return redirect('employer:employer_dashboard')
            else:
                return render(request, 'core/login_employer.html', {
                    'error': 'This login is only for Employers.'
                })

        return render(request, 'core/login_employer.html', {'error': 'Invalid credentials or user type.'})

    return render(request, 'core/login_employer.html')

@login_required
@never_cache
def logout_employer(request):

    logout(request)
    return redirect('home')

@never_cache
def register_employer(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Prevent login until email verification
            user.save()

            # Generate email confirmation link
            current_site = get_current_site(request)
            email_subject = "Confirm Your PESO Sync Account"
            email_body = render_to_string('core/company_email_confirmation.html', {
                'name': user.company_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user),
            })

            print(f"Sending email to: {user.email}")  # ✅ Debugging step
            print(f"Email Subject: {email_subject}")
            print(f"Email Body: {email_body}")
            email = EmailMessage(email_subject, email_body, settings.EMAIL_HOST_USER, [user.email])
            email.send(fail_silently=True)

            messages.success(request, "Account created! Please check your email to verify your account.")
            return redirect('login_employer')
    else:
        form = EmployerRegistrationForm()
    return render(request,  'core/register_employer.html', {'form': form})


