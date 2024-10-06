from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Task

def index(request):
    return render(request, 'todoapp/index.html')

def get_tasks(request):
    tasks = list(Task.objects.values())
    return JsonResponse({'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('name')
        if task_name:
            task = Task.objects.create(name=task_name)
            return JsonResponse({'task': {'id': task.id, 'name': task.name, 'is_completed': task.is_completed}})
    return JsonResponse({'error': 'Task name is required'}, status=400)

def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task_name = request.POST.get('name')
        is_completed = request.POST.get('is_completed')
        
        # Update task name and/or completion status
        if task_name:
            task.name = task_name
        if is_completed is not None:
            task.is_completed = is_completed.lower() == 'true'  # Convert string to boolean

        task.save()
        return JsonResponse({'task': {'id': task.id, 'name': task.name, 'is_completed': task.is_completed}})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return JsonResponse({'result': 'Task deleted successfully'})
