from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

from .models import Task
from .forms import TaskForm, CustomUserCreationForm, CustomAuthenticationForm


@csrf_protect
def register_view(request):
    """
    User registration view with form validation.
    """
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
            return redirect('task_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'tasks/register.html', {'form': form})


@csrf_protect
def login_view(request):
    """
    User login view with session handling.
    """
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                next_page = request.GET.get('next', 'task_list')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'tasks/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    User logout view with session cleanup.
    """
    username = request.user.username
    logout(request)
    messages.success(request, f'Goodbye, {username}! You have been logged out successfully.')
    return redirect('login')


@login_required
def task_list_view(request):
    """
    Read: List all tasks for the logged-in user with filtering and pagination.
    """
    tasks = Task.objects.filter(user=request.user)
    
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    search_query = request.GET.get('search')
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, status='completed').count()
    pending_tasks = Task.objects.filter(user=request.user, status='pending').count()
    
    context = {
        'page_obj': page_obj,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'search_query': search_query,
    }
    
    return render(request, 'tasks/task_list.html', context)


@login_required
@csrf_protect
def task_create_view(request):
    """
    Create: Add a new task with validation.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Create New Task',
        'button_text': 'Create Task'
    })


@login_required
def task_detail_view(request, pk):
    """
    Read: View details of a specific task.
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
@csrf_protect
def task_update_view(request, pk):
    """
    Update: Edit an existing task with validation.
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_detail', pk=task.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Update Task',
        'button_text': 'Update Task',
        'task': task
    })


@login_required
@csrf_protect
@require_http_methods(["POST"])
def task_delete_view(request, pk):
    """
    Delete: Remove a task with confirmation.
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task_title = task.title
    task.delete()
    messages.success(request, f'Task "{task_title}" has been deleted successfully!')
    return redirect('task_list')


@login_required
def dashboard_view(request):
    """
    Dashboard with user statistics and overview.
    """
    user_tasks = Task.objects.filter(user=request.user)
    
    context = {
        'total_tasks': user_tasks.count(),
        'completed_tasks': user_tasks.filter(status='completed').count(),
        'pending_tasks': user_tasks.filter(status='pending').count(),
        'in_progress_tasks': user_tasks.filter(status='in_progress').count(),
        'high_priority_tasks': user_tasks.filter(priority='high').count(),
        'recent_tasks': user_tasks[:5],
    }
    
    return render(request, 'tasks/dashboard.html', context)