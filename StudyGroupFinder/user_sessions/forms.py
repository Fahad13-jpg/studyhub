from django import forms
from .models import StudySession, SessionRSVP

class StudySessionForm(forms.ModelForm):
    """Form for creating and editing study sessions"""
    class Meta:
        model = StudySession
        fields = ['title', 'description', 'date', 'time', 'duration', 'location']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Midterm Preparation Session'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'What will be covered in this session?'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in minutes',
                'min': 15,
                'step': 15
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Library Room 204'
            }),
        }


class RSVPForm(forms.ModelForm):
    """Form for RSVP to sessions"""
    class Meta:
        model = SessionRSVP
        fields = ['status']
        widgets = {
            'status': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            })
        }