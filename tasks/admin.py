from django.contrib import admin
from .models import Category, Task

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'color')
    search_fields = ('name', 'owner__username')
    list_filter = ('owner',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'category', 'status', 'priority', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'owner__username', 'category__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'owner', 'category')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
