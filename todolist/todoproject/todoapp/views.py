from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Task

def index(request):
    return render(request, 'todoapp/index.html')

@login_required
def get_tasks(request):
    # Filter tasks by the logged-in user
    tasks = list(Task.objects.filter(user=request.user).order_by('is_completed').values())
    return JsonResponse({'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('name')
        if task_name:
            # Create task with the logged-in user
            task = Task.objects.create(name=task_name, user=request.user)
            return JsonResponse({'task': {'id': task.id, 'name': task.name, 'is_completed': task.is_completed}})
    return JsonResponse({'error': 'Task name is required'}, status=400)

@login_required
def update_task(request, task_id):
    # Get task by id and make sure it belongs to the logged-in user
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task_name = request.POST.get('name')
        is_completed = request.POST.get('is_completed')

        if task_name:
            task.name = task_name
        if is_completed is not None:
            task.is_completed = is_completed.lower() == 'true'

        task.save()
        return JsonResponse({'task': {'id': task.id, 'name': task.name, 'is_completed': task.is_completed}})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_task(request, task_id):
    # Get task by id and make sure it belongs to the logged-in user
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.delete()
    return JsonResponse({'result': 'Task deleted successfully'})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the main page after login
        else:
            return render(request, 'todoapp/login.html', {'error': 'Invalid username or password'})
    return render(request, 'todoapp/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'todoapp/register.html', {'error': 'Passwords do not match'})

        # Check if username is unique
        if User.objects.filter(username=username).exists():
            return render(request, 'todoapp/register.html', {'error': 'Username already exists'})

        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Automatically log in the user after registration
        login(request, user)

        # Redirect to index page
        return redirect('index')
    return render(request, 'todoapp/register.html')

def logout_view(request):
    """
    Logs out the user and redirects them to the login page.
    """
    logout(request)  # Use Django's built-in logout function
    return redirect('login')  # Redirect to login page after logout
