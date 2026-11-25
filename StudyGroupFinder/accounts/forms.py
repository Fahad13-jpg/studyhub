from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    """
    Extended registration form with first name, last name, and email
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })

        hints = {'username': 'username', 'first_name': 'given-name', 'last_name': 'family-name', 'email': 'email', 'password1': 'new-password', 'password2': 'new-password'}
        labels = {'username': 'Username', 'first_name': 'First name', 'last_name': 'Last name', 'email': 'Email address', 'password1': 'Password', 'password2': 'Confirm password'}
        for name, field in self.fields.items():
            field.label = labels.get(name, field.label)
            field.widget.attrs.update({'autocomplete': hints.get(name, 'off'), 'aria-describedby': f'id_{name}_hint id_{name}_errors'})
        self.fields['username'].help_text = 'The name you’ll use to log in.'
        self.fields['username'].widget.attrs.pop('autofocus', None)
        self.fields['username'].widget.attrs['autocapitalize'] = 'none'
        self.fields['username'].widget.attrs['spellcheck'] = 'false'
        self.fields['password2'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class UserLoginForm(AuthenticationForm):
    """
    Custom login form with Bootstrap styling
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'autocomplete': 'username' if name == 'username' else 'current-password', 'aria-describedby': f'id_{name}_hint id_{name}_errors'})
        self.fields['username'].widget.attrs.update({'autocapitalize': 'none', 'spellcheck': 'false'})
        self.fields['username'].widget.attrs.pop('autofocus', None)



class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile information
    """
    class Meta:
        model = UserProfile
        fields = ['university', 'department', 'semester', 'year', 'phone', 'bio', 'profile_picture']
        widgets = {
            'university': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., University of California'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Computer Science'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-select'
            }),
            'year': forms.Select(attrs={
                'class': 'form-select'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1234567890'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself...',
                'rows': 4
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user information (name, email)
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
