from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='course_pdfs/', blank=True, null=True)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='topic_pdfs/', blank=True, null=True)
    image = models.ImageField(upload_to='topic_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question_text = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question_text

