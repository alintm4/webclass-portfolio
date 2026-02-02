# Django Task Manager - CRUD Application

A complete Task Management CRUD application built with Django featuring user authentication, form validation, and secure session handling.

## 🌟 Features

### Core Functionality
- **Complete CRUD Operations**: Create, Read, Update, and Delete tasks
- **User Authentication**: Secure registration, login, and logout
- **Form Validation**: Client and server-side validation
- **Session Management**: Secure token/session handling with CSRF protection
- **User Isolation**: Each user can only see and manage their own tasks

### Task Management
- **Task Properties**: Title, description, priority (low/medium/high), status (pending/in progress/completed), due date
- **Filtering & Search**: Filter by status, priority, and search by keywords
- **Pagination**: Easy navigation through large task lists
- **Overdue Detection**: Automatic identification of overdue tasks
- **Statistics Dashboard**: View task counts and status overview

### Security Features
- **CSRF Protection**: All forms protected against CSRF attacks
- **Password Validation**: Strong password requirements (min 8 chars, not all numeric)
- **Session Security**: HTTP-only cookies, secure settings for production
- **User Authorization**: Login required decorators for protected views
- **XSS Protection**: Django's built-in template escaping

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation & Setup

### 1. Clone or Extract the Project

```bash
cd task_manager_project
```

### 2. Create a Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Run the Development Server

```bash
python manage.py runserver
```

### 7. Access the Application

Open your browser and navigate to:
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
task_manager_project/
├── manage.py                 # Django management script
├── settings.py              # Project settings
├── urls.py                  # Main URL configuration
├── wsgi.py                  # WSGI configuration
├── requirements.txt         # Python dependencies
├── tasks/                   # Main application
│   ├── __init__.py
│   ├── admin.py            # Admin configuration
│   ├── forms.py            # Form definitions with validation
│   ├── models.py           # Task model
│   ├── urls.py             # App URL patterns
│   ├── views.py            # View functions
│   └── migrations/         # Database migrations
└── templates/              # HTML templates
    ├── base.html           # Base template
    └── tasks/
        ├── dashboard.html
        ├── login.html
        ├── register.html
        ├── task_list.html
        ├── task_form.html
        └── task_detail.html
```

## 🔐 Authentication & Security

### User Registration
- Username validation (min 3 chars, alphanumeric + underscores)
- Email validation (unique emails required)
- Password validation:
  - Minimum 8 characters
  - Cannot be entirely numeric
  - Cannot be too similar to username
  - Cannot be a commonly used password

### Login/Logout
- Secure session-based authentication
- CSRF tokens on all forms
- Session cookies are HTTP-only
- Remember me functionality via session expiry (2 weeks)

### Password Security
- Passwords are hashed using Django's default PBKDF2 algorithm
- Never stored in plain text
- Password validators enforce strong passwords

## 🎨 Form Validation

### Task Form Validation
1. **Title Field**:
   - Required
   - Minimum 3 characters
   - Maximum 200 characters
   - Duplicate check (optional)

2. **Due Date**:
   - Cannot be in the past (for new tasks)
   - Warning if completed task has future due date

3. **Description**:
   - Optional field
   - No length limits

4. **Priority & Status**:
   - Restricted to predefined choices
   - Default values provided

### Registration Form Validation
1. **Username**:
   - Minimum 3 characters
   - Alphanumeric and underscores only
   - Unique across all users

2. **Email**:
   - Valid email format
   - Unique across all users

3. **Password**:
   - Minimum 8 characters
   - Not entirely numeric
   - Not too similar to other personal information
   - Not in common password list

## 📊 Usage Guide

### Creating a Task
1. Click "New Task" button
2. Fill in task details:
   - Title (required)
   - Description (optional)
   - Priority (low/medium/high)
   - Status (pending/in progress/completed)
   - Due date (optional)
3. Click "Create Task"

### Viewing Tasks
- **Dashboard**: Overview with statistics and recent tasks
- **Task List**: Complete list with filtering and search
- **Task Detail**: Full information about a specific task

### Updating a Task
1. Navigate to task detail or list
2. Click "Edit" button
3. Modify task information
4. Click "Update Task"

### Deleting a Task
1. Navigate to task detail or list
2. Click "Delete" button
3. Confirm deletion in modal dialog

### Filtering & Search
- **Search**: Enter keywords in search box
- **Filter by Status**: Select pending/in progress/completed
- **Filter by Priority**: Select low/medium/high
- **Combine Filters**: Use multiple filters simultaneously

## 🔒 Security Best Practices Implemented

1. **CSRF Protection**: All POST forms include CSRF tokens
2. **SQL Injection Prevention**: Django ORM prevents SQL injection
3. **XSS Protection**: Template auto-escaping enabled
4. **Session Security**:
   - HTTP-only cookies
   - SameSite cookie attribute
   - Secure flag for HTTPS (production)
5. **Password Hashing**: PBKDF2 with SHA256
6. **Authorization**: Login required decorators
7. **User Isolation**: Users can only access their own tasks

## 🌐 Production Deployment Checklist

Before deploying to production:

1. **Update settings.py**:
   ```python
   DEBUG = False
   SECRET_KEY = 'your-production-secret-key'  # Generate new key
   ALLOWED_HOSTS = ['yourdomain.com']
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

2. **Use Production Database**:
   - PostgreSQL (recommended)
   - MySQL
   - Configure in settings.py

3. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```

4. **Use Environment Variables**:
   - Store sensitive data in environment variables
   - Use python-decouple or django-environ

5. **Enable HTTPS**:
   - Use SSL/TLS certificate
   - Configure secure cookies

6. **Set Up Logging**:
   - Configure Django logging
   - Monitor application errors

## 🧪 Testing

To test the application:

1. **Create Test Users**:
   - Register multiple users to test isolation
   - Verify each user sees only their tasks

2. **Test CRUD Operations**:
   - Create tasks
   - Update tasks
   - Delete tasks
   - Verify database changes

3. **Test Validation**:
   - Submit invalid forms
   - Verify error messages
   - Test edge cases

4. **Test Authentication**:
   - Login/logout
   - Access protected pages without login
   - Test session expiry

## 📝 API Endpoints

| URL Pattern | View | Description | Method |
|------------|------|-------------|--------|
| `/` | dashboard | User dashboard | GET |
| `/register/` | register | User registration | GET, POST |
| `/login/` | login | User login | GET, POST |
| `/logout/` | logout | User logout | GET |
| `/tasks/` | task_list | List all tasks | GET |
| `/tasks/create/` | task_create | Create new task | GET, POST |
| `/tasks/<id>/` | task_detail | View task details | GET |
| `/tasks/<id>/update/` | task_update | Update task | GET, POST |
| `/tasks/<id>/delete/` | task_delete | Delete task | POST |

## 🐛 Troubleshooting

### Common Issues

1. **Database errors**:
   ```bash
   python manage.py migrate --run-syncdb
   ```

2. **Static files not loading**:
   - Ensure DEBUG=True for development
   - Run collectstatic for production

3. **Session issues**:
   - Clear browser cookies
   - Check SESSION_ENGINE in settings

4. **Form validation errors**:
   - Check form.errors in template
   - Verify model field constraints

## 🤝 Contributing

This is a learning project demonstrating Django CRUD operations with authentication. Feel free to extend it with:
- Task categories/tags
- File attachments
- Team collaboration
- Email notifications
- API endpoints (Django REST Framework)
- Task comments
- Task history/audit log

## 📄 License

This project is created for educational purposes and is free to use and modify.

## 👨‍💻 Author

Created as a demonstration of Django web development with security best practices.

## 🔗 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)