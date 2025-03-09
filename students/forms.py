from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Course, Topic, Question


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role='student')  # Default role is 'student'
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'profile_picture']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


# students/forms.py


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'pdf_file', 'image']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'pdf_file', 'image']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'answer']

