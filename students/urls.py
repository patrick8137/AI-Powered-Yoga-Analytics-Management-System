from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('edit-profile/', views.edit_profile, name='student_edit_profile'),
    path('pay-fees/', views.student_pay_fees, name='student_pay_fees'),
]
