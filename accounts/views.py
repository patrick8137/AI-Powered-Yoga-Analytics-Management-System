from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')

            if user.groups.filter(name='Instructors').exists():
                return redirect('instructor_dashboard')

            if user.groups.filter(name='Students').exists():
                return redirect('student_dashboard')

            messages.error(request, "Role not assigned. Contact admin.")
            return redirect('login')

        messages.error(request, "Invalid credentials")

    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        group, created = Group.objects.get_or_create(name='Students')
        user.groups.add(group)

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')
