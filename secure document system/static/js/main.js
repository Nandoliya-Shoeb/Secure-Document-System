// ============================================
// Secure Signup - Main JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initPasswordToggle();
    initFormValidation();
    initMessageClose();
    initFormAnimations();
    initInputAnimations();
});

// Password Toggle Functionality
function initPasswordToggle() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);
            
            if (passwordInput) {
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    this.textContent = '🙈';
                } else {
                    passwordInput.type = 'password';
                    this.textContent = '👁️';
                }
            }
        });
    });
}

// Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('.auth-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('.submit-btn');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('.form-input');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });
    });
}

// Validate individual field
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name || field.id;
    
    // Remove existing error
    clearFieldError(field);
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        showFieldError(field, 'This field is required.');
        return false;
    }
    
    // Email validation
    if (fieldName.includes('email') && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(field, 'Please enter a valid email address.');
            return false;
        }
    }
    
    // Username validation
    if (fieldName.includes('username') && value) {
        if (value.length < 3) {
            showFieldError(field, 'Username must be at least 3 characters.');
            return false;
        }
        const usernameRegex = /^[a-zA-Z0-9_@.+-]+$/;
        if (!usernameRegex.test(value)) {
            showFieldError(field, 'Username can only contain letters, numbers, and @/./+/-/_');
            return false;
        }
    }
    
    // Password validation
    if (fieldName.includes('password1') && value) {
        if (value.length < 8) {
            showFieldError(field, 'Password must be at least 8 characters.');
            return false;
        }
        
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$/;
        if (!passwordRegex.test(value)) {
            showFieldError(field, 'Password must contain uppercase, lowercase, number, and special character.');
            return false;
        }
    }
    
    // Password confirmation validation
    if (fieldName.includes('password2') && value) {
        const password1 = document.getElementById('id_password1');
        if (password1 && password1.value !== value) {
            showFieldError(field, 'Passwords do not match.');
            return false;
        }
    }
    
    return true;
}

// Show field error
function showFieldError(field, message) {
    field.classList.add('error');
    field.style.borderColor = '#ef4444';
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message shake';
    errorDiv.textContent = message;
    
    const formGroup = field.closest('.form-group');
    if (formGroup) {
        const existingError = formGroup.querySelector('.error-message');
        if (existingError && !existingError.textContent.includes(message)) {
            existingError.textContent = message;
        } else if (!existingError) {
            formGroup.appendChild(errorDiv);
        }
    }
}

// Clear field error
function clearFieldError(field) {
    field.classList.remove('error');
    field.style.borderColor = '';
    
    const formGroup = field.closest('.form-group');
    if (formGroup) {
        const errorMessages = formGroup.querySelectorAll('.error-message');
        errorMessages.forEach(error => {
            // Only remove client-side errors, not server-side ones
            if (!error.textContent.includes('already exists') && 
                !error.textContent.includes('Invalid')) {
                error.remove();
            }
        });
    }
}

// Message Close Functionality
function initMessageClose() {
    const closeButtons = document.querySelectorAll('.close-message');
    
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.closest('.message');
            if (message) {
                message.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => {
                    message.remove();
                }, 300);
            }
        });
    });
    
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            if (message.parentElement) {
                message.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => {
                    message.remove();
                }, 300);
            }
        }, 5000);
    });
}

// Form Animations
function initFormAnimations() {
    const inputs = document.querySelectorAll('.form-input');
    
    inputs.forEach(input => {
        // Focus animation
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        // Blur animation
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Check if input has value on load
        if (input.value) {
            input.parentElement.classList.add('focused');
        }
    });
}

// Input Animations
function initInputAnimations() {
    const inputs = document.querySelectorAll('.form-input');
    
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value) {
                this.style.transform = 'scale(1.01)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 200);
            }
        });
    });
}

// Show Error Function (for global errors)
function showError(message) {
    const messagesContainer = document.querySelector('.messages-container');
    if (!messagesContainer) {
        // Create messages container if it doesn't exist
        const container = document.createElement('div');
        container.className = 'messages-container';
        document.body.appendChild(container);
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'message message-error shake';
    errorDiv.innerHTML = `
        ${message}
        <span class="close-message">&times;</span>
    `;
    
    const container = document.querySelector('.messages-container');
    container.appendChild(errorDiv);
    
    // Re-initialize close button
    const closeBtn = errorDiv.querySelector('.close-message');
    closeBtn.addEventListener('click', function() {
        errorDiv.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            errorDiv.remove();
        }, 300);
    });
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentElement) {
            errorDiv.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                errorDiv.remove();
            }, 300);
        }
    }, 5000);
}

// Add slideOutRight animation to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);



