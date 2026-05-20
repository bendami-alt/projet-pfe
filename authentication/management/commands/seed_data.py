from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from authentication.models import Professor
from students.models import Student

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial data (Superuser, Admin, Professor, Student)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('--- Starting Data Seeding ---'))

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
            self.stdout.write(self.style.SUCCESS('- Superuser "admin" created.'))
        else:
            self.stdout.write(self.style.SUCCESS('- Superuser "admin" updated.'))

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
        self.stdout.write(self.style.SUCCESS('- Utilisateur "platform_admin" créé/mis à jour.'))

        # 3. PROFESSOR
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
                'subject': 'SID'  # Added as it's a required field in the model
            }
        )
        self.stdout.write(self.style.SUCCESS('- Professeur "prof1" créé/mis à jour.'))

        # 4. STUDENT
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
        self.stdout.write(self.style.SUCCESS('- Étudiant "student1" créé/mis à jour.'))

        self.stdout.write(self.style.MIGRATE_HEADING('\n--- Données initiales générées avec succès ---'))

        # FINAL SUMMARY
        self.stdout.write("\n" + "="*40)
        self.stdout.write("RÉSUMÉ DES COMPTES CRÉÉS")
        self.stdout.write("="*40)
        accounts = [
            ("admin", "admin123", "Superuser"),
            ("platform_admin", "admin123", "Admin"),
            ("prof1", "admin123", "Professor"),
            ("student1", "admin123", "Student"),
        ]
        self.stdout.write(f"{'Username':<20} | {'Password':<15} | {'Role':<15}")
        self.stdout.write("-" * 55)
        for username, password, role in accounts:
            self.stdout.write(f"{username:<20} | {password:<15} | {role:<15}")
        self.stdout.write("="*40)
