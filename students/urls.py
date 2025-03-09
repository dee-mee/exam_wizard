from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),

    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/add_topic/', views.add_topic, name='add_topic'),
    path('topics/<int:topic_id>/add_question/', views.add_question, name='add_question'),
    path('courses/<int:course_id>/download_pdf/', views.download_course_pdf, name='download_course_pdf'),
]
