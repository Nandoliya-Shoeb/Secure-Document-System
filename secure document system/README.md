# 💎 Secure & Animated Login/Signup System (Django)

A modern Django-based authentication system with complete security measures, beautiful animations, and responsive design.

## ✨ Features

### 🔐 Security Features
- ✅ No duplicate usernames or emails
- ✅ Passwords are fully hashed using Django's built-in authentication
- ✅ CSRF protection enabled
- ✅ Client-side and server-side validation
- ✅ Strong password requirements (min 8 chars, uppercase, lowercase, number, special character)
- ✅ Secure session management

### 🎨 UI/UX Features
- ✅ Animated gradient background
- ✅ Smooth form transitions and animations
- ✅ Input focus glow effects
- ✅ Error shake animations
- ✅ Responsive design (mobile-friendly)
- ✅ Password visibility toggle
- ✅ Real-time form validation
- ✅ Beautiful message notifications

### 📋 Form Features

#### Signup Form
- Full Name
- Username (unique)
- Email (unique)
- Password (with strength validation)
- Confirm Password (must match)

#### Login Form
- Username/Email (supports both)
- Password

#### Dashboard
- Personalized welcome message
- User information display
- Secure logout

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download
```bash
# Navigate to your project directory
cd "secure signup"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

### Step 7: Access the Application
Open your browser and navigate to:
- **Login Page**: http://127.0.0.1:8000/
- **Signup Page**: http://127.0.0.1:8000/signup/
- **Dashboard**: http://127.0.0.1:8000/dashboard/ (requires login)
- **Admin Panel**: http://127.0.0.1:8000/admin/ (requires superuser)

## 📁 Project Structure

```
secure signup/
├── manage.py
├── requirements.txt
├── README.md
├── secure_signup/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── accounts/
│           ├── base.html
│           ├── login.html
│           ├── signup.html
│           └── dashboard.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## 🔒 Security Implementation

### Password Hashing
- Django automatically hashes passwords using PBKDF2 algorithm
- Passwords are never stored in plain text
- Uses Django's `UserCreationForm` which handles hashing automatically

### CSRF Protection
- All forms include CSRF tokens
- Django middleware validates CSRF tokens on POST requests

### Validation
- **Server-side**: Django forms validate all inputs
- **Client-side**: JavaScript provides real-time feedback
- **Database**: Unique constraints prevent duplicate usernames/emails

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character (!@#$%^&*(),.?":{}|<>)

## 🎨 Customization

### Changing Colors
Edit `static/css/style.css` and modify the CSS variables:
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #10b981;
    --error-color: #ef4444;
}
```

### Adding Features
- The project is modular and easy to extend
- Add new views in `accounts/views.py`
- Add new URLs in `accounts/urls.py`
- Create new templates in `accounts/templates/accounts/`

## 🐛 Troubleshooting

### Issue: Static files not loading
**Solution**: Make sure `STATIC_URL` and `STATICFILES_DIRS` are correctly configured in `settings.py`

### Issue: Database errors
**Solution**: Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: CSRF token errors
**Solution**: Make sure `{% csrf_token %}` is included in all forms

## 📝 Notes

- This project uses SQLite by default (for development)
- For production, consider using PostgreSQL
- Change `SECRET_KEY` in `settings.py` before deploying
- Set `DEBUG = False` in production
- Enable HTTPS and update security settings for production

## 🎯 Technology Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (default) / PostgreSQL (production)
- **Security**: Django Authentication, CSRF Protection

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations accounts
python manage.py migrate
```

### Accessing Admin Panel
1. Create superuser: `python manage.py createsuperuser`
2. Visit: http://127.0.0.1:8000/admin/
3. Login with superuser credentials

## ✅ Checklist

- [x] Custom User Model with full name
- [x] Signup form with validation
- [x] Login form with username/email support
- [x] Password hashing
- [x] CSRF protection
- [x] Client-side validation
- [x] Server-side validation
- [x] Animated UI
- [x] Responsive design
- [x] Dashboard with user info
- [x] Secure logout
- [x] Error handling
- [x] Message notifications

---

**Ready to use!** 🚀 Start the server and begin creating accounts!



