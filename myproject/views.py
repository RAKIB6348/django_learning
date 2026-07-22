from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

ROLES = [
    {"id": "admin", "label": "Admin"},
    {"id": "teacher", "label": "Teacher"},
    {"id": "student", "label": "Student"},
]


def role_login(request):
    if request.user.is_authenticated:
        return _redirect_to_dashboard(request.user)

    if request.method == "POST":
        role = request.POST.get("role", "")
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html", {"active_tab": role, "roles": ROLES})

        error = _validate_role(user, role)
        if error:
            messages.error(request, error)
            return render(request, "login.html", {"active_tab": role, "roles": ROLES})

        login(request, user)
        return _redirect_to_dashboard(user)

    return render(request, "login.html", {"active_tab": "admin", "roles": ROLES})


def _validate_role(user, role):
    if role == "admin":
        if not user.is_superuser and not user.is_staff:
            return "This account is not an Admin account."
    elif role == "teacher":
        if not hasattr(user, "teacher_profile"):
            return "This account is not a Teacher account."
    elif role == "student":
        if not hasattr(user, "student_profile"):
            return "This account is not a Student account."
    return None


def _redirect_to_dashboard(user):
    if user.is_superuser or user.is_staff:
        return redirect("admin:index")
    if hasattr(user, "teacher_profile"):
        return redirect("teacher_dashboard")
    if hasattr(user, "student_profile"):
        return redirect("student_dashboard")
    return redirect("admin:index")


def logout_view(request):
    logout(request)
    return redirect("role_login")


def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("role_login")
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "Access denied. Admins only.")
        return redirect("role_login")
    return render(request, "admin_dashboard.html")


def teacher_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("role_login")
    if not hasattr(request.user, "teacher_profile"):
        messages.error(request, "Access denied. Teachers only.")
        return redirect("role_login")
    return render(request, "teacher_dashboard.html", {"teacher": request.user.teacher_profile})


def student_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("role_login")
    if not hasattr(request.user, "student_profile"):
        messages.error(request, "Access denied. Students only.")
        return redirect("role_login")
    return render(request, "student_dashboard.html", {"student": request.user.student_profile})
