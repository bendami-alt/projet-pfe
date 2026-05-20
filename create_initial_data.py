import os
import django

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from authentication.models import Professor
from students.models import Student

User = get_user_model()

def create_initial_data():
    print("--- Démarrage de la génération des données ---")

    # 1. DJANGO SUPERUSER
    superuser, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@edupredict.com',
            'is_staff': True,
            'is_superuser': True,
            'role': 'admin'
        }
    )
    superuser.set_password('admin123')
    superuser.save()
    if created:
        print("- Superuser 'admin' créé.")
    else:
        print("- Superuser 'admin' mis à jour.")

    # 2. PLATFORM ADMIN
    p_admin, created = User.objects.update_or_create(
        username='platform_admin',
        defaults={
            'first_name': 'Platform',
            'last_name': 'Admin',
            'email': 'platform_admin@edupredict.com',
            'role': 'admin'
        }
    )
    p_admin.set_password('admin123')
    p_admin.save()
    print("- Utilisateur 'platform_admin' créé/mis à jour.")

    # 3. PROFESSEUR DE TEST
    prof_user, created = User.objects.update_or_create(
        username='prof1',
        defaults={
            'first_name': 'Soumai',
            'last_name': 'Laankra',
            'email': 'prof1@edupredict.com',
            'role': 'professor'
        }
    )
    prof_user.set_password('admin123')
    prof_user.save()

    prof_profile, p_created = Professor.objects.update_or_create(
        user=prof_user,
        defaults={
            'employee_id': 'PROF001',
            'department': 'SID',
            'subject': 'SID'
        }
    )
    print("- Professeur 'prof1' créé/mis à jour.")

    # 4. ÉTUDIANT DE TEST
    student_user, created = User.objects.update_or_create(
        username='student1',
        defaults={
            'first_name': 'Akram',
            'last_name': 'Bne',
            'email': 'student1@edupredict.com',
            'role': 'student'
        }
    )
    student_user.set_password('admin123')
    student_user.save()

    student_profile, s_created = Student.objects.update_or_create(
        user=student_user,
        defaults={
            'professor': prof_profile,
            'midterm_score': 95,
            'assignment_completion': 95,
            'attendance_rate': 98,
            'study_hours': 9,
            'motivation': 'Elevée',
            'parental_support': 'Fort',
            'previous_grade': 'A',
            'learning_style': 'Visuel'
        }
    )
    print("- Étudiant 'student1' créé/mis à jour.")

    print("\n--- Données initiales générées avec succès ---")

    # RÉSUMÉ FINAL
    print("\n" + "="*55)
    print(f"{'Username':<20} | {'Password':<15} | {'Role':<15}")
    print("-" * 55)
    accounts = [
        ("admin", "admin123", "Superuser"),
        ("platform_admin", "admin123", "Admin"),
        ("prof1", "admin123", "Professor"),
        ("student1", "admin123", "Student"),
    ]
    for username, password, role in accounts:
        print(f"{username:<20} | {password:<15} | {role:<15}")
    print("="*55)

if __name__ == '__main__':
    create_initial_data()
