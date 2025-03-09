from audioop import reverse
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import CustomUser

from capstone import settings
from .tokens import generate_token  # Custom token generator
from employer.models import accreditation_document_storage
from jobseeker.models import ResumeDocument, JobseekerProfile, Education, Employment

from employer.models import AccreditationRequest
from .forms import *

app_name = 'core'


# Create your views here.

def home(request):
    return render(request, f"{app_name}/home.html")
@login_required
def dashboard(request):
    return render(request, f"{app_name}/index.html")
@login_required
def companies(request):
    requests = AccreditationRequest.objects.all()
    return render(request, f"{app_name}/companies.html", {"requests": requests})
@login_required
def accredited_companies(request):
    return render(request, f"{app_name}/accredited-companies.html")
@login_required
def jobs(request):
    return render(request, f"{app_name}/jobs.html")
@login_required
def employees(request):
    return render(request, f"{app_name}/employees.html")
@login_required
def seminars(request):
    return render(request, f"{app_name}/seminars.html")
@login_required
def profile(request):
    return render(request, f"{app_name}/users-profile.html")
@login_required
def job_trends(request):
    return render(request, f"{app_name}/job-trends.html")
@login_required
def tools(request):
    return render(request, f"{app_name}/tools.html")
@login_required
def faqs(request):
    return render(request, f"{app_name}/pages-faq.html")
@login_required
def analytics(request):
    return render(request, f"{app_name}/analytics.html")
@login_required
def job_analytics(request):
    return render(request, f"{app_name}/job-analytics.html")
def employer_dashboard(request):
    return render(request, 'employer/employer_dashboard.html')
def job_seeker_dashboard(request):
    return render(request, 'jobseeker/job_seeker_dashboard.html')
def login_peso(request):
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

        return render(request, 'core/login_peso.html', {'error': 'Invalid credentials or user type.'})
    return render(request, 'core/login_peso.html')

@login_required
def logout_peso(request):
    logout(request)
    return redirect('home')



def login_job_seeker(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if not user.is_active:
                return render(request, 'core/login_job_seeker.html', {'error': 'Please verify your email before logging in.'})
            if user.user_type == 'JOB_SEEKER':
                login(request, user)
                return redirect('job_seeker_dashboard')

        return render(request, 'core/login_job_seeker.html', {'error': 'Invalid credentials or user type.'})
    return render(request, 'core/login_job_seeker.html')


@login_required
def logout_job_seeker(request):
    logout(request)
    return redirect('home')

def register_job_seeker(request):
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Prevent login until email verification
            user.save()

            # Generate email confirmation link
            current_site = get_current_site(request)
            email_subject = "Confirm Your PESO Sync Account"
            email_body = render_to_string('core/email_confirmation.html', {
                'name': user.first_name,  # ✅ Add this line
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
            return redirect('login_job_seeker')

    else:
        form = JobSeekerRegistrationForm()
    return render(request, 'core/register_job_seeker.html', {'form': form})

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

def register_peso(request):
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

@login_required
def logout_employer(request):
    logout(request)
    return redirect('home')

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
        return redirect('login_job_seeker')  # Change to appropriate login page
    else:
        return render(request, 'core/activation_failed.html')

def login_employer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if not user.is_active:
                return render(request, 'core/login_employer.html', {'error': 'Please verify your email before logging in.'})
            if user.user_type == 'EMPLOYER':
                login(request, user)
                return redirect('employer:employer_dashboard')

        return render(request, 'core/login_employer.html', {'error': 'Invalid credentials or user type.'})
    return render(request, 'core/login_employer.html')




