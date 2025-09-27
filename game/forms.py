from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with validation requirements"""
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username (min 5 characters)',
            'required': True
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password',
            'required': True
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'required': True
        })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Check minimum length
        if len(username) < 5:
            raise ValidationError("Username must be at least 5 characters long.")
        
        # Check for both upper and lower case letters
        if not (any(c.isupper() for c in username) and any(c.islower() for c in username)):
            raise ValidationError("Username must contain both uppercase and lowercase letters.")
        
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        # Check minimum length
        if len(password) < 5:
            raise ValidationError("Password must be at least 5 characters long.")
        
        # Check for alphabetic characters
        if not any(c.isalpha() for c in password):
            raise ValidationError("Password must contain at least one alphabetic character.")
        
        # Check for numeric characters
        if not any(c.isdigit() for c in password):
            raise ValidationError("Password must contain at least one numeric character.")
        
        # Check for special characters
        special_chars = ['$', '%', '*', '@']
        if not any(c in special_chars for c in password):
            raise ValidationError("Password must contain at least one special character ($, %, *, @).")
        
        return password


class GuessForm(forms.Form):
    """Form for submitting word guesses"""
    guess = forms.CharField(
        max_length=5,
        min_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control guess-input',
            'placeholder': 'Enter 5-letter word',
            'maxlength': '5',
            'pattern': '[A-Z]{5}',
            'style': 'text-transform: uppercase; text-align: center; font-size: 1.5rem; font-weight: bold; letter-spacing: 0.2rem;',
            'autocomplete': 'off'
        })
    )

    def clean_guess(self):
        guess = self.cleaned_data.get('guess', '').upper().strip()
        
        # Check length
        if len(guess) != 5:
            raise ValidationError("Guess must be exactly 5 letters long.")
        
        # Check if all characters are letters
        if not guess.isalpha():
            raise ValidationError("Guess must contain only letters.")
        
        return guess


class AdminReportForm(forms.Form):
    """Form for admin reports"""
    REPORT_CHOICES = [
        ('daily', 'Daily Report'),
        ('user', 'User Report'),
    ]
    
    report_type = forms.ChoiceField(
        choices=REPORT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text="Select date for daily report"
    )
    
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select user for user report"
    )

    def clean(self):
        cleaned_data = super().clean()
        report_type = cleaned_data.get('report_type')
        date = cleaned_data.get('date')
        user = cleaned_data.get('user')

        if report_type == 'daily' and not date:
            raise ValidationError("Date is required for daily report.")
        
        if report_type == 'user' and not user:
            raise ValidationError("User is required for user report.")

        return cleaned_data
