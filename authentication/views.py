from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def landing_view(request):
    if request.user.is_authenticated:
        return redirect_based_on_role(request.user)
    return render(request, 'authentication/landing.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect_based_on_role(request.user)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect_based_on_role(user)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')

def redirect_based_on_role(user):
    if user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'professor':
        return redirect('professor_dashboard')
    elif user.role == 'student':
        return redirect('student_dashboard')
    else:
        return redirect('login')
