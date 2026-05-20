import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_platform.settings')
django.setup()

from authentication.models import User, Professor
from students.models import Student

def populate():
    print("--- Start Population ---")

    # 1. Update ADMIN
    admin_user = User.objects.filter(username='ADMIN').first()
    if admin_user:
        admin_user.role = 'admin'
        admin_user.save()
        print(f"Updated ADMIN role to 'admin'")

    # 2. Create Professor
    prof_user, created = User.objects.get_or_create(
        username='prof1',
        defaults={'first_name': 'Jean', 'last_name': 'Dupont', 'role': 'professor'}
    )
    if created:
        prof_user.set_password('password123')
        prof_user.save()
    
    prof_profile, created = Professor.objects.get_or_create(
        user=prof_user,
        defaults={'subject': 'Mathematics'}
    )
    print(f"Professor 'prof1' (Jean Dupont) ready.")

    # 3. Create Students
    student_data = [
        ('student_a', 'Alice', 'Smith', 85, 95, 98, 12, 'A', 'Elevée', 'Fort', 'Visuel'),
        ('student_b', 'Bob', 'Johnson', 65, 70, 80, 8, 'B', 'Moyenne', 'Moyen', 'Auditif'),
        ('student_c', 'Charlie', 'Brown', 45, 50, 60, 4, 'C', 'Faible', 'Faible', 'Kinesthésique'),
        ('ikram', 'Ikram', 'Belkacem', 78, 88, 92, 10, 'B', 'Moyenne', 'Fort', 'Lecture/Ecriture'),
        ('LALA', 'Lala', 'Zahra', 55, 62, 75, 6, 'C', 'Faible', 'Moyen', 'Visuel'),
    ]

    for username, fname, lname, midterm, assign, attend, hrs, prev, motiv, parent, style in student_data:
        u, created = User.objects.get_or_create(
            username=username,
            defaults={'first_name': fname, 'last_name': lname, 'role': 'student'}
        )
        if created:
            u.set_password('password123')
            u.save()
        
        # Create/Update Student Profile
        s, created = Student.objects.get_or_create(
            user=u,
            defaults={
                'professor': prof_profile,
                'midterm_score': midterm,
                'assignment_completion': assign,
                'attendance_rate': attend,
                'study_hours': hrs,
                'previous_grade': prev,
                'motivation': motiv,
                'parental_support': parent,
                'learning_style': style
            }
        )
        if not created:
            # Update existing to match data
            s.professor = prof_profile
            s.midterm_score = midterm
            s.assignment_completion = assign
            s.attendance_rate = attend
            s.study_hours = hrs
            s.previous_grade = prev
            s.motivation = motiv
            s.parental_support = parent
            s.learning_style = style
            s.save()
            
        print(f"Student '{username}' ({fname} {lname}) ready. Prediction: {s.prediction}")

    print("--- Population Complete ---")

if __name__ == '__main__':
    populate()
