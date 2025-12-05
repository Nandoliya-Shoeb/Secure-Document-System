# 🚀 Quick Start Guide

## Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Server**
   ```bash
   python manage.py runserver
   ```

5. **Access Application**
   - Login: http://127.0.0.1:8000/
   - Signup: http://127.0.0.1:8000/signup/
   - Dashboard: http://127.0.0.1:8000/dashboard/
   - Admin: http://127.0.0.1:8000/admin/

## Features Checklist

✅ Secure password hashing  
✅ CSRF protection  
✅ Unique username & email validation  
✅ Strong password requirements  
✅ Client-side & server-side validation  
✅ Animated UI with smooth transitions  
✅ Responsive design  
✅ Username/Email login support  
✅ Beautiful error messages  
✅ Password visibility toggle  

## Test Credentials

After creating an account, you can login with:
- Username OR Email
- Your password

## Troubleshooting

**Static files not loading?**
- Make sure you're running `python manage.py runserver`
- Check that `static/` folder exists with `css/` and `js/` subfolders

**Database errors?**
- Run: `python manage.py makemigrations accounts`
- Then: `python manage.py migrate`

**Import errors?**
- Make sure you're in the project root directory
- Activate virtual environment if using one

---

**Ready to go!** 🎉



