from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UserForm, CourseForm, TopicForm, QuestionForm
from .models import UserProfile, Course, Topic, Question
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponse


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

    return render(request, 'students/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def student_dashboard(request):
    return render(request, 'students/dashboard.html')

def check_user_role(user, allowed_roles):
    user_profile = UserProfile.objects.get(user=user)
    return user_profile.role in allowed_roles

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'students/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'students/course_detail.html', {'course': course})

@login_required
def add_course(request):
    if not check_user_role(request.user, ['teacher', 'admin']):
        return HttpResponseForbidden("You do not have permission to add courses.")

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'students/add_course.html', {'form': form})

@login_required
def add_topic(request, course_id):
    if not check_user_role(request.user, ['teacher', 'admin']):
        return HttpResponseForbidden("You do not have permission to add topics.")

    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.course = course
            topic.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = TopicForm()
    return render(request, 'students/add_topic.html', {'form': form, 'course': course})

@login_required
def add_question(request, topic_id):
    if not check_user_role(request.user, ['teacher', 'admin']):
        return HttpResponseForbidden("You do not have permission to add questions.")

    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.topic = topic
            question.save()
            return redirect('course_detail', course_id=topic.course.id)
    else:
        form = QuestionForm()
    return render(request, 'students/add_question.html', {'form': form, 'topic': topic})

@login_required
def download_course_pdf(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Generate PDF logic here
    # For simplicity, this example just returns a placeholder response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{course.name}.pdf"'
    # Add PDF generation logic here
    return response
