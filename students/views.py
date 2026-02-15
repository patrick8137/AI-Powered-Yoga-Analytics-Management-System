from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django.db.models import Sum

from .models import StudentProfile, MonthlyFee
from .forms import StudentProfileForm
from instructors.models import (
    InstructorStudent,
    Attendance,
    PracticeLog,
    LearningDocument,
)
from ai_engine.models import AIInsight
from students.models import FeeSetting   


# ---------------- STUDENT DASHBOARD ----------------
@login_required
def student_dashboard(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    instructor = None
    mapping = (
        InstructorStudent.objects
        .select_related('instructor__user')
        .filter(student=student)
        .first()
    )
    if mapping:
        instructor = mapping.instructor

    today = now().date()
    month_start = today.replace(day=1)
    attendance_labels = []
    attendance_data = []
    practice_labels = []
    practice_data = []

    for i in range(4):
        week_start = month_start + timedelta(days=i * 7)
        week_end = week_start + timedelta(days=6)

        total_days = Attendance.objects.filter(
            student=student,
            date__range=(week_start, week_end)
        ).count()

        present_days = Attendance.objects.filter(
            student=student,
            date__range=(week_start, week_end),
            present=True
        ).count()

        attendance_labels.append(f"Week {i + 1}")
        attendance_data.append(
            round((present_days / total_days) * 100) if total_days else 0
        )

        week_practice = (
            PracticeLog.objects.filter(
                student=student,
                date__range=(week_start, week_end)
            ).aggregate(total=Sum('hours'))['total']
        ) or 0

        practice_labels.append(f"Week {i + 1}")
        practice_data.append(float(week_practice))

    month_total_days = Attendance.objects.filter(
        student=student,
        date__range=(month_start, today)
    ).count()

    month_present_days = Attendance.objects.filter(
        student=student,
        date__range=(month_start, today),
        present=True
    ).count()

    attendance_percent = (
        round((month_present_days / month_total_days) * 100)
        if month_total_days else 0
    )

    monthly_practice_hours = (
        PracticeLog.objects
        .filter(student=student, date__range=(month_start, today))
        .aggregate(total=Sum('hours'))
        .get('total') or 0
    )

    monthly_practice_hours = float(monthly_practice_hours)

    avg_weekly_practice = monthly_practice_hours / 4 if monthly_practice_hours else 0
    practice_score = min((avg_weekly_practice / 5) * 100, 100)

    progress_score = round(
        (attendance_percent * 0.6) +
        (practice_score * 0.4)
    )

    ai_status = "AI Pending"
    ai_message = "AI analysis will appear once enough data is available."

    insight = getattr(student, 'ai_insight', None)
    if insight:
        ai_status = (
            "Improving" if insight.cluster == 0 else
            "Stable" if insight.cluster == 1 else
            "Needs Attention"
        )
        ai_message = insight.message or ai_message

    fee_setting = FeeSetting.objects.first()
    fee_amount = fee_setting.monthly_fee_amount if fee_setting else 1000

    monthly_fee, created = MonthlyFee.objects.get_or_create(
        student=student,
        month=month_start,
        defaults={'amount': fee_amount}
    )
    if monthly_fee.amount == 0:
        monthly_fee.amount = fee_amount
        monthly_fee.save()

    show_fee_warning = not monthly_fee.is_paid
    documents = LearningDocument.objects.filter(
        instructor__instructorstudent__student=student
    )

    context = {
        'student': student,
        'instructor': instructor,
        'attendance_percent': attendance_percent,
        'monthly_practice_hours': monthly_practice_hours,
        'progress_score': progress_score,
        'attendance_labels': attendance_labels,
        'attendance_data': attendance_data,
        'practice_labels': practice_labels,
        'practice_data': practice_data,
        'ai_status': ai_status,
        'ai_message': ai_message,
        'monthly_fee': monthly_fee,
        'show_fee_warning': show_fee_warning,
        'documents': documents,
    }

    return render(request, 'students/dashboard.html', context)


# ---------------- EDIT PROFILE ----------------
@login_required
def edit_profile(request):
    student = request.user.studentprofile

    if request.method == 'POST':
        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=student,
            user=request.user
        )

        if form.is_valid():
            profile = form.save(commit=False)

            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()

            profile.save()
            messages.success(request, "Profile updated successfully")
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=student, user=request.user)

    return render(request, 'students/edit_profile.html', {'form': form})


# ---------------- PAY MONTHLY FEES ----------------
@login_required
def student_pay_fees(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    current_month = now().date().replace(day=1)

    fee = MonthlyFee.objects.filter(
        student=student,
        month=current_month,
        is_paid=False
    ).first()

    if request.method == 'POST' and fee:
        fee.mark_as_paid()
        messages.success(request, "Monthly fee paid successfully.")
        return redirect('student_dashboard')

    return render(request, 'students/pay_fees.html', {'fee': fee})
