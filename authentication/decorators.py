from django.contrib.auth.decorators import user_passes_test

def admin_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.role == 'admin',
        login_url='login'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def professor_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.role == 'professor',
        login_url='login'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def staff_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.role == 'admin' or u.role == 'professor'),
        login_url='login'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def student_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.role == 'student',
        login_url='login'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
