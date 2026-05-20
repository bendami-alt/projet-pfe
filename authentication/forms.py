from django import forms
from .models import User, Professor
from students.models import Student

# Only admin creates users, so RegistrationForm is no longer needed.
