from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.checks import messages
import csv

from admins.models import Admin
from .forms import UserProfileForm, UserForm, CourseForm, TopicForm, QuestionForm
from .models import UserProfile, Course, Topic, Question
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string



def student_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')  # Redirect to student dashboard
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

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
    topics = course.topic_set.all()
    questions = []
    for topic in topics:
        questions.extend(topic.question_set.all())
    return render(request, 'students/course_detail.html', {'course': course, 'topics': topics, 'questions': questions})


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
def search_questions(request):
    qualification = request.GET.get('qualification')
    unit = request.GET.get('unit')
    question_type = request.GET.get('question_type')
    theme = request.GET.get('theme')

    # Logic to search questions based on the input parameters
    # For now, we'll just return a placeholder response
    return render(request, 'students/search_results.html', {
        'qualification': qualification,
        'unit': unit,
        'question_type': question_type,
        'theme': theme
    })

@login_required
def generate_pdf(request):
    # Logic to generate PDF based on the selected criteria
    html = render_to_string('students/pdf_template.html', {})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="questions.pdf"'
    PDF = HTML(string=html).write_pdf()
    response.write(PDF)
    return response

@login_required
def download_course_pdf(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Generate PDF logic here
    # For simplicity, this example just returns a placeholder response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{course.name}.pdf"'
    # Add PDF generation logic here
    return response

@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    questions = topic.question_set.all()
    return render(request, 'students/topic_detail.html', {'topic': topic, 'questions': questions})




# Export CSV
def export_admins_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="admins.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Email", "Phone Number"])

    for admin in Admin.objects.all():
        writer.writerow([admin.name, admin.email, admin.phone_number])

    return response
def custom_logout(request):
    # Manually clear the session
    if 'username' in request.session:
        del request.session['username']
    # Optionally, you can clear the entire session
    request.session.flush()
    return redirect('landing')  # Redirect to the landing page