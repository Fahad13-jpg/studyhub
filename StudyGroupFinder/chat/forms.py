from django import forms
from .models import GroupMessage

class MessageForm(forms.ModelForm):
    """Form for sending messages"""
    class Meta:
        model = GroupMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your message here...',
                'required': True
            })
        }