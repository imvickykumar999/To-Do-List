from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Task

# Register the Task model with custom admin configurations
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_completed', 'user')  # Display user field
    search_fields = ('name', 'user__username')  # Enable search for task name and username
    list_filter = ('is_completed', 'user')  # Filter by completion status and user
    ordering = ('id',)


# Unregister the original User model to customize it
admin.site.unregister(User)

# Register the customized User model using UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Display fields in the list view of users
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    # Enable search functionality for the username, email, and name fields
    search_fields = ('username', 'email', 'first_name', 'last_name')
    # Enable filters for user status
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
