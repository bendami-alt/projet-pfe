from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from authentication.decorators import admin_required, professor_required, student_required, staff_required
from authentication.models import Professor
from .models import Student
from .forms import StudentAddForm


@admin_required
def admin_dashboard(request):
    students = Student.objects.all().select_related('user', 'professor__user')
    professors_count = Professor.objects.count()
    students_count = students.count()

    # Prediction distribution (ensure all keys exist)
    predictions = students.values('prediction').annotate(count=Count('prediction'))
    prediction_dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for p in predictions:
        if p['prediction'] in prediction_dist:
            prediction_dist[p['prediction']] = p['count']
    
    total_predictions = sum(prediction_dist.values())

    context = {
        'students': students,
        'professors_count': professors_count,
        'students_count': students_count,
        'prediction_dist': prediction_dist,
        'total_predictions': total_predictions,
        'grade_a_count': prediction_dist['A'],
        'grade_b_count': prediction_dist['B'],
        'grade_c_count': prediction_dist['C'],
        'grade_d_count': prediction_dist['D'],
    }
    return render(request, 'students/admin_dashboard.html', context)


@professor_required
def professor_dashboard(request):
    professor = getattr(request.user, 'professor_profile', None)
    if not professor:
        logout(request)
        messages.error(request, "No professor profile found. Please contact admin.")
        return redirect('login')

    students = Student.objects.filter(professor=professor).select_related('user')
    
    # Prediction distribution for this professor (ensure all keys exist)
    predictions = students.values('prediction').annotate(count=Count('prediction'))
    prediction_dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for p in predictions:
        if p['prediction'] in prediction_dist:
            prediction_dist[p['prediction']] = p['count']

    context = {
        'professor': professor,
        'students': students,
        'students_count': students.count(),
        'prediction_dist': prediction_dist,
        'total_predictions': sum(prediction_dist.values()),
        'grade_a_count': prediction_dist['A'],
        'grade_b_count': prediction_dist['B'],
        'grade_c_count': prediction_dist['C'],
        'grade_d_count': prediction_dist['D'],
    }
    return render(request, 'students/professor_dashboard.html', context)


@staff_required
def add_student(request):
    professor = getattr(request.user, 'professor_profile', None)

    if request.method == 'POST':
        form = StudentAddForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                # If admin, use the selected professor from the form
                if request.user.role == 'admin':
                    assigned_prof = form.cleaned_data.get('professor_choice')
                else:
                    assigned_prof = professor
                
                form.save(professor=assigned_prof)
                messages.success(request, "✅ Student created and prediction generated successfully!")
                
                if request.user.role == 'admin':
                    return redirect('admin_student_list')
                return redirect('professor_dashboard')
            except Exception as e:
                messages.error(request, f"Error saving student: {e}")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = StudentAddForm(user=request.user)

    return render(request, 'students/add_student.html', {'form': form})


@student_required
def student_dashboard(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        logout(request)
        messages.error(request, "No student profile found. Please contact your professor.")
        return redirect('login')

    return render(request, 'students/student_dashboard.html', {'student': student})


@admin_required
def professor_list(request):
    professors = Professor.objects.all().select_related('user')
    return render(request, 'students/professor_list.html', {'professors': professors})


@admin_required
def add_professor(request):
    if request.method == 'POST':
        from .forms import ProfessorForm
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Professor added successfully.")
            return redirect('professor_list')
    else:
        from .forms import ProfessorForm
        form = ProfessorForm()
    return render(request, 'students/add_professor.html', {'form': form})


@admin_required
def delete_professor(request, pk):
    professor = Professor.objects.get(pk=pk)
    user = professor.user
    professor.delete()
    user.delete()
    messages.success(request, "Professor and their account deleted.")
    return redirect('professor_list')


@admin_required
def professor_detail(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    students = professor.students.all().select_related('user')
    
    # Statistics
    predictions = students.values('prediction').annotate(count=Count('prediction'))
    stats = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for p in predictions:
        if p['prediction'] in stats:
            stats[p['prediction']] = p['count']
            
    context = {
        'professor': professor,
        'students': students,
        'stats': stats,
        'total_students': students.count(),
    }
    return render(request, 'students/professor_detail.html', context)


@admin_required
def edit_professor(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    from .forms import ProfessorEditForm
    
    if request.method == 'POST':
        form = ProfessorEditForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Professor updated successfully!")
            return redirect('professor_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProfessorEditForm(instance=professor)
        
    return render(request, 'students/edit_professor.html', {
        'form': form,
        'professor': professor
    })


@admin_required
def admin_student_list(request):
    students = Student.objects.all().select_related('user', 'professor__user')
    return render(request, 'students/admin_student_list.html', {'students': students})


from .pdf_utils import render_to_pdf
from django.utils import timezone

@login_required
def export_student_report(request, pk=None):
    if request.user.role == 'student':
        student = request.user.student_profile
    else:
        if not pk:
            return redirect('admin_dashboard')
        student = Student.objects.get(pk=pk)
    
    context = {
        'student': student,
        'date': timezone.now(),
    }
    return render_to_pdf('reports/student_report.html', context)


@admin_required
def export_admin_report(request):
    students = Student.objects.all()
    professors_count = Professor.objects.count()
    students_count = students.count()
    
    predictions = students.values('prediction').annotate(count=Count('prediction'))
    prediction_dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for p in predictions:
        if p['prediction'] in prediction_dist:
            prediction_dist[p['prediction']] = p['count']
    
    context = {
        'students': students,
        'students_count': students_count,
        'professors_count': professors_count,
        'prediction_dist': prediction_dist,
        'date': timezone.now(),
    }
    return render_to_pdf('reports/admin_report.html', context)


@login_required
def export_professor_report(request, pk=None):
    if request.user.role == 'professor':
        professor = request.user.professor_profile
    else:
        if not pk:
            return redirect('admin_dashboard')
        professor = Professor.objects.get(pk=pk)
        
    students = Student.objects.filter(professor=professor)
    predictions = students.values('prediction').annotate(count=Count('prediction'))
    prediction_dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for p in predictions:
        if p['prediction'] in prediction_dist:
            prediction_dist[p['prediction']] = p['count']
    
    context = {
        'professor': professor,
        'students': students,
        'students_count': students.count(),
        'grade_a_count': prediction_dist['A'],
        'grade_b_count': prediction_dist['B'],
        'grade_c_count': prediction_dist['C'],
        'grade_d_count': prediction_dist['D'],
        'date': timezone.now(),
    }
    return render_to_pdf('reports/professor_report.html', context)


@admin_required
def admin_student_pdf(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = {
        'student': student,
        'date': timezone.now(),
        'is_admin_report': True
    }
    # messages.success(request, f"Rapport PDF généré avec succès pour {student.user.get_full_name() or student.user.username}")
    return render_to_pdf('reports/student_report.html', context)


@admin_required
def admin_edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    from .forms import StudentEditForm
    
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Étudiant modifié avec succès.")
            return redirect('admin_student_list')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = StudentEditForm(instance=student)
    
    return render(request, 'students/edit_student.html', {
        'form': form,
        'student': student
    })


@admin_required
def admin_delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    
    if request.method == 'POST':
        student_name = student.user.get_full_name() or student.user.username
        student.delete()
        user.delete()
        messages.success(request, f"Étudiant {student_name} supprimé avec succès.")
        return redirect('admin_student_list')
    
    return redirect('admin_student_list')


@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    
    if user.role == 'student':
        context['student'] = getattr(user, 'student_profile', None)
    elif user.role == 'professor':
        context['professor'] = getattr(user, 'professor_profile', None)
        
    return render(request, 'students/profile.html', context)


@professor_required
def professor_student_list(request):
    professor = getattr(request.user, 'professor_profile', None)
    if not professor:
        return redirect('login')
        
    students = Student.objects.filter(professor=professor).select_related('user')
    return render(request, 'students/professor_student_list.html', {
        'students': students,
        'professor': professor
    })
