from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import validate_image_file
import re

User = get_user_model()


class SignupForm(UserCreationForm):
    """Signup form with full validation"""
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Full Name',
            'autocomplete': 'name'
        }),
        help_text='Enter your full name'
    )
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username',
            'autocomplete': 'username'
        }),
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email',
            'autocomplete': 'email'
        })
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
            'autocomplete': 'new-password'
        }),
        help_text='Password must be at least 8 characters with uppercase, lowercase, number, and special character.'
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm Password',
            'autocomplete': 'new-password'
        }),
        help_text='Enter the same password as before, for verification.'
    )
    
    class Meta:
        model = User
        fields = ('full_name', 'username', 'email', 'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('A user with this username already exists.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        
        # Check for uppercase
        if not re.search(r'[A-Z]', password1):
            raise ValidationError('Password must contain at least one uppercase letter.')
        
        # Check for lowercase
        if not re.search(r'[a-z]', password1):
            raise ValidationError('Password must contain at least one lowercase letter.')
        
        # Check for number
        if not re.search(r'\d', password1):
            raise ValidationError('Password must contain at least one number.')
        
        # Check for special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise ValidationError('Password must contain at least one special character.')
        
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError({
                'password2': 'Passwords do not match.'
            })
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    """Profile form for secure document/id details"""
    class Meta:
        model = User
        fields = [
            'full_name',
            'document_id',
            'pan_number',
            'aadhaar_number',
            'address',
            'id_document_photo',
            'pan_document_photo',
            'address_proof_photo',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'document_id': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Document ID'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'PAN / Tax ID'}),
            'aadhaar_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Aadhaar / National ID'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Address', 'rows': 3}),
        }

    def clean_pan_number(self):
        pan = self.cleaned_data.get('pan_number', '').upper().strip()
        if pan and len(pan) < 8:
            raise ValidationError('PAN/Tax ID seems too short.')
        return pan

    def clean_aadhaar_number(self):
        aadhaar = self.cleaned_data.get('aadhaar_number', '').strip()
        if aadhaar and not aadhaar.isdigit():
            raise ValidationError('Aadhaar/National ID should be numeric.')
        if aadhaar and len(aadhaar) not in (0, 12):
            raise ValidationError('Aadhaar/National ID should be 12 digits.')
        return aadhaar

    def clean(self):
        cleaned = super().clean()
        for field in ('id_document_photo', 'pan_document_photo', 'address_proof_photo'):
            file = self.files.get(field)
            if file:
                validate_image_file(file)
        return cleaned


class LoginForm(AuthenticationForm):
    """Login form with username/email support"""
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username or Email',
            'autocomplete': 'username'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
            'autocomplete': 'current-password'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Allow login with either username or email
        return username
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Try to find user by username first, then by email
            user = None
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    pass
            
            if user is None:
                raise ValidationError('Invalid username/email or password.')
            
            if not user.check_password(password):
                raise ValidationError('Invalid username/email or password.')
            
            if not user.is_active:
                raise ValidationError('This account is inactive.')
            
            # Set the username to the actual username for Django authentication
            self.cleaned_data['username'] = user.username
            self.user_cache = user
        
        return self.cleaned_data

