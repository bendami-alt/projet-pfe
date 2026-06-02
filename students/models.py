from django.db import models
from authentication.models import User, Professor


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    
    student_id = models.CharField(max_length=50, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)

    # Academic data (made optional for initial registration)
    midterm_score = models.FloatField(default=0.0)
    assignment_completion = models.FloatField(default=0.0)
    attendance_rate = models.FloatField(default=0.0)
    study_hours = models.FloatField(default=0.0)

    # Categorical fields (made optional for initial registration)
    previous_grade = models.CharField(max_length=50, blank=True, default='C')
    motivation = models.CharField(max_length=50, blank=True, default='Medium')
    parental_support = models.CharField(max_length=50, blank=True, default='Medium')
    learning_style = models.CharField(max_length=50, blank=True, default='Visual')

    # ML Prediction result
    prediction = models.CharField(max_length=10, blank=True, default='')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        """
        Auto-generate ML prediction whenever the student record is created or updated.
        The import is inside the method to avoid circular imports during app startup.
        """
        # Only update prediction if called normally (not via update_fields to avoid infinite recursion)
        if 'update_fields' not in kwargs:
            try:
                from ml.utils import predict_student
                self.prediction = predict_student(self)
            except Exception as e:
                print(f"[ML] Prediction error for {getattr(self, 'user_id', '?')}: {e}")
                if not self.prediction:
                    self.prediction = 'NA'

        super().save(*args, **kwargs)

        # After saving the student, record the prediction history
        if 'update_fields' not in kwargs and self.prediction:
            PredictionHistory.objects.create(
                student=self,
                predicted_grade=self.prediction,
                midterm_score=self.midterm_score,
                attendance_rate=self.attendance_rate,
                study_hours=self.study_hours,
                previous_grade=self.previous_grade,
                motivation=self.motivation,
                parental_support=self.parental_support,
                learning_style=self.learning_style
            )

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    class Meta:
        ordering = ['user__username']


class PredictionHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='prediction_history')
    predicted_grade = models.CharField(max_length=10)
    midterm_score = models.FloatField()
    attendance_rate = models.FloatField()
    study_hours = models.FloatField()
    previous_grade = models.CharField(max_length=50, blank=True)
    motivation = models.CharField(max_length=50, blank=True)
    parental_support = models.CharField(max_length=50, blank=True)
    learning_style = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.predicted_grade} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-created_at']

