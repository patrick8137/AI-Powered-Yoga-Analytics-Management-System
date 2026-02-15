from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('students/', views.instructor_students, name='instructor_students'),
    path('daily-activity/', views.daily_activity, name='daily_activity'),
    path('attendance-history/', views.attendance_history, name='attendance_history'),
    path('upload/', views.upload_document, name='upload_document'),
    path('delete-document/<int:doc_id>/', views.delete_document, name='delete_document'),
]
