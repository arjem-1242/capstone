from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from core.models import CustomUser
from .models import Applicant, JobPosting
from core.forms import *
from .models import *
from .forms import *
from django.urls import reverse
from pesostaff.models import AccreditationRequestApproval
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.

def employer_dashboard(request):
    # Query to get all accreditation requests, or specific ones based on your requirement
    return render(request, 'employer/employer_dashboard.html')

def employer_about(request):
    return render(request, 'employer/about.html')

def employer_services(request):
    return render(request, 'employer/services.html')

def employer_contact(request):
    return render(request, 'employer/contact.html')

def employer_service_detail_1(request):
    return render(request, 'employer/service_1.html')

def employer_service_detail_2(request):
    return render(request, 'employer/service_2.html')

def employer_service_detail_3(request):
    return render(request, 'employer/service_3.html')

def employer_service_detail_4(request):
    return render(request, 'employer/service_4.html')

def employer_service_detail_5(request):
    return render(request, 'employer/service_5.html')

def employer_service_detail_6(request):
    return render(request, 'employer/service_6.html')
def employer_faqs(request):
    return render(request, 'employer/faqs.html')

@login_required
def logout_employer(request):
    logout(request)
    return redirect('home')

# CompanyProfile view
@login_required
def update_company_profile(request, pk):
    company_profile = get_object_or_404(CompanyProfile, id=pk)
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, instance=company_profile)
        if form.is_valid():
            form.save()
            # return redirect('company_profile_detail', pk=pk)  # Redirect to detail view or list view
            return redirect(reverse('employer:company_profile_detail', kwargs={'pk': pk}))  # Use reverse with redirect
    else:
        form = CompanyProfileForm(instance=company_profile)
    return render(request, 'employer/update_company_profile.html', {'form': form})

@login_required
def employer_profile_view(request):
    user = request.user

    if user.user_type != 'EMPLOYER':
        return HttpResponseForbidden("You are not authorized to view this page.")

    return render(request, 'employer/profile.html', {'employer': user})


# class ChangePasswordForm(forms.Form):
#     old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
#     new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
#     confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")
#
#     def clean(self):
#         cleaned_data = super().clean()
#         new_password = cleaned_data.get("new_password")
#         confirm_password = cleaned_data.get("confirm_password")
#
#         if new_password and confirm_password and new_password != confirm_password:
#             raise forms.ValidationError("New passwords do not match.")
#         return cleaned_data


@login_required
def change_password_view(request):
    if request.user.user_type != 'EMPLOYER':
        messages.error(request, "You are not authorized to change the password.")
        return redirect('home')

    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get("old_password")
            new_password = form.cleaned_data.get("new_password")

            if not request.user.check_password(old_password):
                messages.error(request, "Old password is incorrect.")
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Keep user logged in
                messages.success(request, "Your password has been successfully updated.")
                return redirect(reverse ("employer:employer_profile_view"))
    else:
        form = ChangePasswordForm()

    return render(request, "employer/change_password.html", {"form": form})


# JobPosting views
@login_required
def create_job_posting(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            # Get the company profile of the logged-in user
            try:
                employer = CompanyProfile.objects.get(user=request.user)
            except CompanyProfile.DoesNotExist:
                messages.error(request, "You need a company profile to post a job.")
                return redirect(reverse('employer:create_job_posting'))

            # Check if accreditation request is approved
            accreditation_request = get_object_or_404(AccreditationRequest, company_profile=employer)
            if accreditation_request.status != 'Approved':
                messages.error(request, "Your accreditation request must be approved before posting a job.")
                return redirect(reverse('employer:create_job_posting'))

            # Save the job posting
            job_posting = form.save(commit=False)
            job_posting.company = employer  # Assign the company profile
            job_posting.save()

            messages.success(request, "Job posting created successfully.")
            return redirect('employer:create_job_posting')
    else:
        form = JobPostingForm()

    return render(request, 'employer/create_job_posting.html', {'form': form})


@login_required
def job_posting_list(request):
    # Get the logged-in employer's company profile
    try:
        employer = CompanyProfile.objects.get(user=request.user)
    except CompanyProfile.DoesNotExist:
        messages.error(request, "You must have a company profile to view job postings.")
        return redirect('employer:employer_dashboard')

    # Filter job postings for the logged-in employer's company
    job_postings = JobPosting.objects.filter(company=employer)

    context = {
        'job_postings': job_postings
    }

    return render(request, 'employer/job_posting_list.html', context)

@login_required
def update_job_posting(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job_posting)
        if form.is_valid():
            form.save()
            # return redirect('job_posting_list')
            return redirect(reverse('employer:job_posting_list'))  # Use reverse with redirect
    else:
        form = JobPostingForm(instance=job_posting)
    return render(request, 'employer/update_job_posting.html', {'form': form})

@login_required
def create_accreditation_request(request):
    if request.method == 'POST':
        form = AccreditationRequestForm(request.POST, request.FILES)
        if form.is_valid():
            # Set the company_profile to the logged-in user's company profile
            company_profile = CompanyProfile.objects.get(user=request.user)

            # Check if there's already an unreviewed accreditation request for this company
            existing_request = AccreditationRequest.objects.filter(
                company_profile=company_profile,
                status__in=['Pending', 'In Review']  # Adjust according to your status choices
            ).first()

            if existing_request:
                # If there's an unreviewed request, return an error or a message
                form.add_error(None, "You already have an accreditation request in review.")
                return render(request, 'employer/create_accreditation_request.html', {'form': form})

            # No existing unreviewed request, proceed with saving the new one
            accreditation_request = form.save(commit=False)  # Don't save to the database yet
            accreditation_request.company_profile = company_profile  # Assign company profile
            accreditation_request.status = 'Pending'  # Assuming the default status is 'Pending'
            accreditation_request.save()  # Now save the object to the database

            return redirect('employer:employer_dashboard')
    else:
        form = AccreditationRequestForm()

    return render(request, 'employer/create_accreditation_request.html', {'form': form})

def load_accreditation_form_fields(request):
    company_type = request.GET.get('company_type')
    form = AccreditationRequestForm(initial={'company_type': company_type})

    return render(request, 'employer/accreditation_form_fields.html', {'form': form})

@login_required
def update_accreditation_request(request, pk):
    accreditation_request = get_object_or_404(AccreditationRequest, pk=pk)
    if request.method == 'POST':
        form = AccreditationRequestForm(request.POST, request.FILES, instance=accreditation_request)
        if form.is_valid():
            form.save()
            # return redirect('accreditation_request_list')
            return redirect(reverse('employer:accreditation_request_list'))
    else:
        form = AccreditationRequestForm(instance=accreditation_request)
    return render(request, 'employer/update_accreditation_request.html', {'form': form})

# Applicant views
@login_required
def update_applicant_resume(request):
    try:
        applicant = Applicant.objects.get(user=request.user)
    except Applicant.DoesNotExist:
        # return redirect('create_applicant')  # Redirect to applicant creation if needed
        return redirect(reverse('employer:create_applicant'))

    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            form.save()
            # return redirect('applicant_detail')  # Change to your detail view
            return redirect(reverse('employer:create_applicant'))
    else:
        form = ApplicantForm(instance=applicant)
    return render(request, 'employer/update_applicant_resume.html', {'form': form})

# SavedCandidate views
@login_required
def save_candidate(request, job_id, applicant_id):
    job_posting = get_object_or_404(JobPosting, id=job_id)
    applicant = get_object_or_404(Applicant, id=applicant_id)
    
    SavedCandidate.objects.create(job_posting=job_posting, applicant=applicant)
    # return redirect('saved_candidates_list')  # Change to your list view
    return redirect(reverse('employer:saved_candidates_list'))


@login_required
def accreditation_request_overview(request):
    try:
        employer = CompanyProfile.objects.get(user=request.user)
    except CompanyProfile.DoesNotExist:
        messages.error(request, "You must have a company profile to view accreditation requests.")
        return redirect('employer:dashboard')

    # Debug: print the employer's company profile
    print(f"Employer company profile: {employer}")

    # Filter accreditation requests for the logged-in employer's company profile
    accreditation_requests = AccreditationRequest.objects.filter(company_profile=employer)
    print(f"Filtered accreditation requests: {accreditation_requests}")  # Debugging line

    # Check if any accreditation requests were found
    if not accreditation_requests.exists():
        print("No accreditation requests found for this employer.")

    # Continue with the rest of the code...
    requests_with_approval = []
    for acc_request in accreditation_requests:
        approval = AccreditationRequestApproval.objects.filter(accreditation_request=acc_request).first()
        comments = approval.comments if approval else 'No comments'
        requests_with_approval.append({
            'company': acc_request.company,
            'status': acc_request.get_status_display(),
            'comments': comments
        })

    context = {
        'accreditation_requests': requests_with_approval
    }

    return render(request, 'employer/accreditation_request_overview.html', context)

