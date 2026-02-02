from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils import timezone


class Task(models.Model):
    """
    Task model representing a user's task with CRUD operations.
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tasks'
    )
    
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3, "Title must be at least 3 characters long")]
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional detailed description of the task"
    )
    
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="Optional due date for the task"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def is_overdue(self):
        """Check if task is overdue."""
        if self.due_date and self.status != 'completed':
            return self.due_date < timezone.now().date()
        return False
    
    def clean(self):
        """Custom validation."""
        from django.core.exceptions import ValidationError
        
        if self.due_date and self.due_date < timezone.now().date():
            if not self.pk:
                raise ValidationError({
                    'due_date': 'Due date cannot be in the past for new tasks.'
                })