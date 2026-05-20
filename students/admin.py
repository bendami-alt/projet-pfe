from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'get_full_name', 'get_username', 'professor', 
        'midterm_score', 'attendance_rate', 'study_hours',
        'previous_grade', 'prediction'
    ]
    list_filter = ['prediction', 'professor', 'motivation', 'learning_style']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['prediction']
    ordering = ['user__username']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Full Name'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
