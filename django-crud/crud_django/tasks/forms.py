from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):
    """
    Form for creating and updating tasks with custom validation.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task description (optional)',
                'rows': 4
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def clean_title(self):
        """Validate title field."""
        title = self.cleaned_data.get('title')
        
        if not title:
            raise ValidationError("Title is required.")
        
        if len(title.strip()) < 3:
            raise ValidationError("Title must be at least 3 characters long.")
        
        if len(title) > 200:
            raise ValidationError("Title cannot exceed 200 characters.")
        
        if self.instance.pk is None:
            user = self.instance.user if hasattr(self.instance, 'user') else None
            if user and Task.objects.filter(user=user, title__iexact=title).exists():
                raise ValidationError("You already have a task with this title.")
        
        return title.strip()
    
    def clean_due_date(self):
        """Validate due date field."""
        due_date = self.cleaned_data.get('due_date')
        
        if due_date:
            if not self.instance.pk and due_date < timezone.now().date():
                raise ValidationError("Due date cannot be in the past.")
        
        return due_date
    
    def clean(self):
        """Cross-field validation."""
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        due_date = cleaned_data.get('due_date')
        
        if status == 'completed' and due_date and due_date > timezone.now().date():
            self.add_error('due_date', 'Warning: Task is marked completed but due date is in the future.')
        
        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user registration form with additional validation.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        """Validate email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email
    
    def clean_username(self):
        """Validate username."""
        username = self.cleaned_data.get('username')
        
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        
        if not username.isalnum() and '_' not in username:
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        
        return username
    
    def save(self, commit=True):
        """Save user with email."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom login form with styled widgets.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    
    def clean(self):
        """Add custom authentication validation."""
        cleaned_data = super().clean()
        return cleaned_data