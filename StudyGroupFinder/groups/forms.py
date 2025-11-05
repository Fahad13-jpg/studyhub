from django import forms
from .models import StudyGroup, JoinRequest

class StudyGroupForm(forms.ModelForm):
    """Form for creating and editing study groups"""
    class Meta:
        model = StudyGroup
        fields = ['name', 'course_name', 'course_code', 'description', 'study_topics', 
                  'max_capacity', 'meeting_days', 'meeting_time', 'meeting_location', 'group_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Advanced Calculus Study Group'}),
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Calculus II'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., MATH 202'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your study group...'}),
            'study_topics': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List main topics covered...'}),
            'max_capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 3, 'max': 10}),
            'meeting_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Monday, Wednesday, Friday'}),
            'meeting_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'meeting_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Library Room 204'}),
            'group_type': forms.Select(attrs={'class': 'form-select'}),
        }


class JoinRequestForm(forms.ModelForm):
    """Form for submitting join requests to private groups"""
    class Meta:
        model = JoinRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Why do you want to join this group? (optional)'
            })
        }