from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Professor
from students.models import Student

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student Profile'
    fk_name = 'user'

class ProfessorInline(admin.StackedInline):
    model = Professor
    can_delete = False
    verbose_name_plural = 'Professor Profile'
    fk_name = 'user'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    
    
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_username', 'subject', 'get_student_count']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'subject']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Name'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_student_count(self, obj):
        return obj.students.count()
    get_student_count.short_description = 'Students'
