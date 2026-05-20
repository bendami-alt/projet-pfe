from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('professor-dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('add/', views.add_student, name='add_student'),
    
    # Professor Management (Admin)
    path('professors/', views.professor_list, name='professor_list'),
    path('professors/add/', views.add_professor, name='add_professor'),
    path('professors/<int:pk>/', views.professor_detail, name='professor_detail'),
    path('professors/<int:pk>/edit/', views.edit_professor, name='edit_professor'),
    path('professors/delete/<int:pk>/', views.delete_professor, name='delete_professor'),
    path('admin-students/', views.admin_student_list, name='admin_student_list'),
    path('admin/students/<int:student_id>/pdf/', views.admin_student_pdf, name='admin_student_pdf'),
    path('admin/students/<int:student_id>/edit/', views.admin_edit_student, name='admin_edit_student'),
    path('admin/students/<int:student_id>/delete/', views.admin_delete_student, name='admin_delete_student'),
    
    # PDF Exports
    path('export/admin/', views.export_admin_report, name='export_admin_report'),
    path('export/professor/<int:pk>/', views.export_professor_report, name='export_professor_report'),
    path('export/professor/', views.export_professor_report, name='export_my_professor_report'),
    path('export/student/<int:pk>/', views.export_student_report, name='export_student_report'),
    path('export/student/', views.export_student_report, name='export_my_report'),
    path('profile/', views.profile, name='profile'),
    path('my-students/', views.professor_student_list, name='professor_student_list'),
]
