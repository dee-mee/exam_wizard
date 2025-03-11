from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from students.models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UserForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.role == 'student':
                    return redirect('student_dashboard')
                elif user_profile.role == 'teacher':
                    return redirect('teacher_dashboard')
                elif user_profile.role == 'admin':
                    return redirect('admin_dashboard')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def custom_logout(request):
    logout(request)
    return render(request, 'registration/logout.html')


def landing_page(request):
    return render(request, 'landing.html')


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})




@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
