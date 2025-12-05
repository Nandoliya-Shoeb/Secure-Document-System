from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm, ProfileForm


def signup_view(request):
    """Signup view with validation"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """Login view with validation"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # Get user from form's user_cache (set in clean method)
            user = form.user_cache
            login(request, user)
            messages.success(request, f'Welcome back, {user.full_name}!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username/email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def dashboard_view(request):
    """Dashboard view with user info"""
    return render(request, 'accounts/dashboard.html', {
        'user': request.user
    })


@login_required
def profile_view(request):
    """Profile page to manage secure document/id details"""
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated securely.')
            return redirect('accounts:profile')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def documents_view(request):
    """List and manage uploaded documents."""
    user = request.user

    if request.method == 'POST':
        doc_type = request.POST.get('doc_type')
        field_map = {
            'id': 'id_document_photo',
            'pan': 'pan_document_photo',
            'address': 'address_proof_photo',
        }
        field_name = field_map.get(doc_type)
        if field_name:
            _delete_document_file(user, field_name)
            setattr(user, field_name, None)
            user.save(update_fields=[field_name])
            messages.success(request, 'Document deleted.')
        else:
            messages.error(request, 'Invalid document type.')
        return redirect('accounts:documents')

    docs = [
        {'label': 'ID Document', 'field': user.id_document_photo, 'key': 'id'},
        {'label': 'PAN / Tax', 'field': user.pan_document_photo, 'key': 'pan'},
        {'label': 'Address Proof', 'field': user.address_proof_photo, 'key': 'address'},
    ]

    return render(request, 'accounts/documents.html', {'user': user, 'docs': docs})


def _delete_document_file(user, field_name: str):
    """Delete the file from storage safely."""
    file_field = getattr(user, field_name, None)
    if file_field and file_field.name:
        storage = file_field.storage
        if storage.exists(file_field.name):
            storage.delete(file_field.name)


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

