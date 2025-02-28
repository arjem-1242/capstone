import pytesseract
from django import forms

from jobseeker.models import JobseekerProfile, ResumeDocument

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows


class JobseekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobseekerProfile
        fields = ['location', 'contact', 'phone' ]  # Add other fields you want to edit


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = ResumeDocument
        fields = ['resume']


class DateForm(forms.Form):
    date_field = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )



