"""
Tests for the Task Management application.
Run with: python manage.py test tasks
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Task
from .forms import TaskForm, CustomUserCreationForm


class TaskModelTest(TestCase):
    """Test cases for Task model."""
    
    def setUp(self):
        """Set up test user and task."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            priority='high',
            status='pending',
            due_date=timezone.now().date() + timedelta(days=7)
        )
    
    def test_task_creation(self):
        """Test task creation."""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.user, self.user)
        self.assertEqual(self.task.priority, 'high')
        self.assertEqual(self.task.status, 'pending')
    
    def test_task_str_method(self):
        """Test task string representation."""
        expected = f"{self.task.title} ({self.task.get_status_display()})"
        self.assertEqual(str(self.task), expected)
    
    def test_task_is_overdue(self):
        """Test is_overdue method."""
        self.assertFalse(self.task.is_overdue())
        
        overdue_task = Task.objects.create(
            user=self.user,
            title='Overdue Task',
            status='pending',
            due_date=timezone.now().date() - timedelta(days=1)
        )
        self.assertTrue(overdue_task.is_overdue())
        
        overdue_task.status = 'completed'
        overdue_task.save()
        self.assertFalse(overdue_task.is_overdue())


class TaskFormTest(TestCase):
    """Test cases for Task forms."""
    
    def setUp(self):
        """Set up test user."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_valid_task_form(self):
        """Test valid task form."""
        form_data = {
            'title': 'Valid Task',
            'description': 'Valid description',
            'priority': 'medium',
            'status': 'pending',
            'due_date': timezone.now().date() + timedelta(days=5)
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_task_form_title_too_short(self):
        """Test task form with short title."""
        form_data = {
            'title': 'AB',  # Too short
            'priority': 'low',
            'status': 'pending'
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_task_form_past_due_date(self):
        """Test task form with past due date."""
        form_data = {
            'title': 'Task with past date',
            'priority': 'low',
            'status': 'pending',
            'due_date': timezone.now().date() - timedelta(days=1)
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)


class UserRegistrationFormTest(TestCase):
    """Test cases for user registration form."""
    
    def test_valid_registration_form(self):
        """Test valid registration form."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_password_mismatch(self):
        """Test registration with password mismatch."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123',
            'password2': 'DifferentPass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_duplicate_email(self):
        """Test registration with duplicate email."""
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpass123'
        )
        form_data = {
            'username': 'newuser',
            'email': 'existing@example.com',  # Duplicate
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class AuthenticationViewsTest(TestCase):
    """Test cases for authentication views."""
    
    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_view_get(self):
        """Test login view GET request."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/login.html')
    
    def test_login_view_post_success(self):
        """Test successful login."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_view_post_failure(self):
        """Test failed login."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_logout_view(self):
        """Test logout view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_register_view_get(self):
        """Test registration view GET request."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/register.html')
    
    def test_register_view_post_success(self):
        """Test successful registration."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(User.objects.filter(username='newuser').exists())


class TaskCRUDViewsTest(TestCase):
    """Test cases for Task CRUD views."""
    
    def setUp(self):
        """Set up test client, user, and task."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            priority='medium',
            status='pending'
        )
    
    def test_task_list_view(self):
        """Test task list view."""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertContains(response, 'Test Task')
    
    def test_task_list_view_requires_login(self):
        """Test task list requires authentication."""
        self.client.logout()
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_task_create_view_get(self):
        """Test task create view GET request."""
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
    
    def test_task_create_view_post(self):
        """Test task creation."""
        response = self.client.post(reverse('task_create'), {
            'title': 'New Task',
            'description': 'New Description',
            'priority': 'high',
            'status': 'pending',
            'due_date': timezone.now().date() + timedelta(days=7)
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Task.objects.filter(title='New Task').exists())
    
    def test_task_detail_view(self):
        """Test task detail view."""
        response = self.client.get(reverse('task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertContains(response, 'Test Task')
    
    def test_task_update_view_get(self):
        """Test task update view GET request."""
        response = self.client.get(reverse('task_update', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
    
    def test_task_update_view_post(self):
        """Test task update."""
        response = self.client.post(reverse('task_update', args=[self.task.pk]), {
            'title': 'Updated Task',
            'priority': 'high',
            'status': 'completed'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, 'completed')
    
    def test_task_delete_view(self):
        """Test task deletion."""
        task_id = self.task.pk
        response = self.client.post(reverse('task_delete', args=[task_id]))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(Task.objects.filter(pk=task_id).exists())
    
    def test_user_cannot_access_other_user_task(self):
        """Test user isolation."""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        other_task = Task.objects.create(
            user=other_user,
            title='Other User Task',
            priority='low',
            status='pending'
        )
        
        response = self.client.get(reverse('task_detail', args=[other_task.pk]))
        self.assertEqual(response.status_code, 404)  # Not found


class DashboardViewTest(TestCase):
    """Test cases for dashboard view."""
    
    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Create test tasks
        Task.objects.create(
            user=self.user,
            title='Task 1',
            status='completed',
            priority='high'
        )
        Task.objects.create(
            user=self.user,
            title='Task 2',
            status='pending',
            priority='medium'
        )
    
    def test_dashboard_view(self):
        """Test dashboard view."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/dashboard.html')
        self.assertEqual(response.context['total_tasks'], 2)
        self.assertEqual(response.context['completed_tasks'], 1)
        self.assertEqual(response.context['pending_tasks'], 1)


class SecurityTest(TestCase):
    """Test security features."""
    
    def setUp(self):
        """Set up test client and users."""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass456'
        )
    
    def test_csrf_protection(self):
        """Test CSRF protection on forms."""
        self.client.login(username='user1', password='pass123')
        
        response = self.client.post(reverse('task_create'), {
            'title': 'Test Task'
        })
        self.assertIn(response.status_code, [200, 302])
    
    def test_login_required_decorator(self):
        """Test login required on protected views."""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)  # Success
    
    def test_user_isolation(self):
        """Test users can only see their own tasks."""
        task1 = Task.objects.create(
            user=self.user1,
            title='User 1 Task',
            priority='high',
            status='pending'
        )
        task2 = Task.objects.create(
            user=self.user2,
            title='User 2 Task',
            priority='low',
            status='pending'
        )
        
        self.client.login(username='user1', password='pass123')
        
        response = self.client.get(reverse('task_detail', args=[task1.pk]))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('task_detail', args=[task2.pk]))
        self.assertEqual(response.status_code, 404)