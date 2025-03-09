from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Course, Topic, Question

class CustomAdminSite(admin.AdminSite):
    site_header = 'Exam Wizard Administration'
    site_title = 'Exam Wizard Admin Portal'
    index_title = 'Welcome to Exam Wizard Admin Portal'

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite(name='customadmin')

# Register the User model with the custom admin site
custom_admin_site.register(User, UserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'full_name', 'email')
    search_fields = ('user__username', 'full_name', 'email')
    list_filter = ('role',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['role'].choices = [
            ('teacher', 'Teacher'),
            ('student', 'Student'),
        ]
        return form

custom_admin_site.register(UserProfile, UserProfileAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    list_filter = ('course',)
    search_fields = ('title',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'topic')
    list_filter = ('topic',)
    search_fields = ('question_text',)

# Register models under custom admin site
custom_admin_site.register(Course, CourseAdmin)
custom_admin_site.register(Topic, TopicAdmin)
custom_admin_site.register(Question, QuestionAdmin)

# Remove unnecessary admin.site.register calls
