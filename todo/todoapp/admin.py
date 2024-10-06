from django.contrib import admin
from .models import Task

# Register the Task model to make it available in the Django admin site
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('id', 'name', 'is_completed')
    # Enable search functionality for name field
    search_fields = ('name',)
    # Enable filter by completion status
    list_filter = ('is_completed',)
    # Order tasks by id
    ordering = ('id',)
