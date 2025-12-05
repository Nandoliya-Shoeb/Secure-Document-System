from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import os
import uuid


def validate_image_file(file):
    """Validate uploaded image size and type for security."""
    max_size = 5 * 1024 * 1024  # 5 MB
    allowed_mime = {'image/jpeg', 'image/png', 'image/webp'}
    allowed_ext = {'.jpg', '.jpeg', '.png', '.webp'}

    if file.size and file.size > max_size:
        raise ValidationError(f'File too large (>{max_size // (1024 * 1024)}MB).')

    content_type = getattr(file, 'content_type', '')
    ext = os.path.splitext(file.name)[1].lower()

    if content_type and content_type not in allowed_mime:
        raise ValidationError('Only JPEG, PNG, or WEBP images are allowed.')

    if ext and ext not in allowed_ext:
        raise ValidationError('Invalid file extension. Use JPEG, PNG, or WEBP.')


def user_document_path(instance, filename, kind: str):
    """Generate per-user upload path with a randomized filename."""
    ext = os.path.splitext(filename)[1].lower()
    safe_ext = ext if ext else '.bin'
    unique_name = f"{uuid.uuid4().hex}{safe_ext}"
    user_part = instance.pk or instance.username or 'temp'
    return os.path.join('documents', str(user_part), kind, unique_name)


class CustomUser(AbstractUser):
    """Custom User model with full name field"""
    full_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=False)
    document_id = models.CharField(max_length=100, blank=True, help_text="Internal document/id reference")
    pan_number = models.CharField(max_length=20, blank=True, help_text="PAN (India) or Tax ID")
    aadhaar_number = models.CharField(max_length=20, blank=True, help_text="Aadhaar or National ID")
    address = models.TextField(blank=True)
    id_document_photo = models.ImageField(
        upload_to=lambda instance, filename: user_document_path(instance, filename, 'id'),
        validators=[validate_image_file],
        blank=True,
        null=True,
    )
    pan_document_photo = models.ImageField(
        upload_to=lambda instance, filename: user_document_path(instance, filename, 'pan'),
        validators=[validate_image_file],
        blank=True,
        null=True,
    )
    address_proof_photo = models.ImageField(
        upload_to=lambda instance, filename: user_document_path(instance, filename, 'address'),
        validators=[validate_image_file],
        blank=True,
        null=True,
    )
    
    # Make username unique
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username


