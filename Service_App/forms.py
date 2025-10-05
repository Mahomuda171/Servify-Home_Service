# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import Booking, SubService
from django.utils import timezone


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'user_type', 'address', 'phn_Num')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 3}),
            'phn_Num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
           model = User
           fields = ['username', 'email', 'address', 'phn_Num']
class WorkerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'phn_Num', 'skills', 'experience', 'is_available']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 3}),
            'phn_Num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'skills': forms.SelectMultiple(attrs={'class': 'form-control','rows': 3}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of Experience'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BookingForm(forms.ModelForm):
    scheduled_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = Booking
        fields = ['scheduled_date', 'address', 'description']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter service address'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any specific requirements?'}),
        }
    
    def clean_scheduled_date(self):
        scheduled_date = self.cleaned_data['scheduled_date']
        if scheduled_date < timezone.now():
            raise forms.ValidationError("Scheduled date cannot be in the past.")
        return scheduled_date