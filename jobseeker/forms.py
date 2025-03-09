import cv2
from PIL import Image, UnidentifiedImageError
import spacy
import numpy as np
import pytesseract
from django import forms
from django.core.exceptions import ValidationError

from core.models import CustomUser
from jobseeker.models import JobseekerProfile, ResumeDocument
from io import BytesIO


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


class JobSeekerChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data


