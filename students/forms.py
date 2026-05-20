from django import forms
from .models import Student
from authentication.models import User


PREVIOUS_GRADE_CHOICES = [
    ('A', 'A — Excellent'),
    ('B', 'B — Good'),
    ('C', 'C — Average'),
    ('D', 'D — Poor'),
]

MOTIVATION_CHOICES = [
    ('Elevée', 'Élevée (High)'),
    ('Moyenne', 'Moyenne (Medium)'),
    ('Faible', 'Faible (Low)'),
]

PARENTAL_SUPPORT_CHOICES = [
    ('Fort', 'Fort (Strong)'),
    ('Moyen', 'Moyen (Medium)'),
    ('Faible', 'Faible (Low)'),
]

LEARNING_STYLE_CHOICES = [
    ('Visuel', 'Visuel'),
    ('Auditif', 'Auditif'),
    ('Kinesthésique', 'Kinesthésique'),
    ('Lecture/Ecriture', 'Lecture/Écriture'),
]


class StudentAddForm(forms.Form):
    # Account fields
    username = forms.CharField(
        max_length=150, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Min. 8 characters'}),
        required=True
    )
    first_name = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )


    professor_choice = forms.ModelChoiceField(
        queryset=None, required=False, label="Assign Professor",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        from authentication.models import Professor
        self.fields['professor_choice'].queryset = Professor.objects.all()
        if user and user.role != 'admin':
            self.fields['professor_choice'].widget = forms.HiddenInput()
            self.fields['professor_choice'].required = False

    # Numeric academic fields
    midterm_score = forms.FloatField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'})
    )
    assignment_completion = forms.FloatField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'})
    )
    attendance_rate = forms.FloatField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'})
    )
    study_hours = forms.FloatField(
        min_value=0, max_value=40,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0', 'max': '40'})
    )

    # Categorical fields
    previous_grade = forms.ChoiceField(
        choices=PREVIOUS_GRADE_CHOICES, initial='B',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    motivation = forms.ChoiceField(
        choices=MOTIVATION_CHOICES, initial='Moyenne',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    parental_support = forms.ChoiceField(
        choices=PARENTAL_SUPPORT_CHOICES, initial='Moyen',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    learning_style = forms.ChoiceField(
        choices=LEARNING_STYLE_CHOICES, initial='Visuel',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please choose another.")
        return email


    def save(self, commit=True, professor=None):
        """Create user + student in one transaction and auto-generate prediction."""
        # Create the Django User
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data.get('first_name', ''),
            last_name=self.cleaned_data.get('last_name', ''),
            role='student'
        )

        # Create the Student profile
        student = Student(
            user=user,
            professor=professor,
            midterm_score=self.cleaned_data['midterm_score'],
            assignment_completion=self.cleaned_data['assignment_completion'],
            attendance_rate=self.cleaned_data['attendance_rate'],
            study_hours=self.cleaned_data['study_hours'],
            previous_grade=self.cleaned_data['previous_grade'],
            motivation=self.cleaned_data['motivation'],
            parental_support=self.cleaned_data['parental_support'],
            learning_style=self.cleaned_data['learning_style'],
        )

        if commit:
            # student.save() triggers ML prediction automatically via model's save()
            student.save()

        return student


class ProfessorForm(forms.Form):
    username = forms.CharField(
        max_length=150, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True
    )
    first_name = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    subject = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mathematics'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data.get('first_name', ''),
            last_name=self.cleaned_data.get('last_name', ''),
            role='professor'
        )
        from authentication.models import Professor
        professor = Professor.objects.create(
            user=user,
            subject=self.cleaned_data['subject']
        )
        return professor


class StudentEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = [
            'professor', 'midterm_score', 'assignment_completion',
            'attendance_rate', 'study_hours', 'previous_grade', 
            'motivation', 'parental_support', 'learning_style'
        ]
        widgets = {
            'professor': forms.Select(attrs={'class': 'form-select'}),
            'midterm_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'assignment_completion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'attendance_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'study_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'previous_grade': forms.Select(choices=PREVIOUS_GRADE_CHOICES, attrs={'class': 'form-select'}),
            'motivation': forms.Select(choices=MOTIVATION_CHOICES, attrs={'class': 'form-select'}),
            'parental_support': forms.Select(choices=PARENTAL_SUPPORT_CHOICES, attrs={'class': 'form-select'}),
            'learning_style': forms.Select(choices=LEARNING_STYLE_CHOICES, attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        student = super().save(commit=False)
        if commit:
            # Update User fields
            student.user.first_name = self.cleaned_data['first_name']
            student.user.last_name = self.cleaned_data['last_name']
            student.user.save()
            student.save()
        return student


class ProfessorEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        from authentication.models import Professor
        model = Professor
        fields = ['department', 'employee_id', 'subject']
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        professor = super().save(commit=False)
        if commit:
            # Update User fields
            professor.user.first_name = self.cleaned_data['first_name']
            professor.user.last_name = self.cleaned_data['last_name']
            professor.user.email = self.cleaned_data['email']
            professor.user.save()
            professor.save()
        return professor
