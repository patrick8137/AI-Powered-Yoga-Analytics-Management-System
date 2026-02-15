from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Avg, Sum
from .forms import DailyActivityForm, LearningDocumentForm
from .models import (
    InstructorProfile,
    Attendance,
    PracticeLog,
    LearningDocument,
    InstructorStudent,
)
from ai_engine.models import AIInsight

@login_required
def instructor_dashboard(request):
    instructor = get_object_or_404(InstructorProfile, user=request.user)

    students = InstructorStudent.objects.filter(instructor=instructor)

    last_7_days = now().date() - timedelta(days=7)

    avg_practice = (
        PracticeLog.objects.filter(
            student__instructorstudent__instructor=instructor,
            date__gte=last_7_days
        ).aggregate(avg=Avg('hours'))['avg']
    ) or 0

    avg_practice = round(float(avg_practice), 1)

    attendance_labels = []
    attendance_trend = []

    for i in range(6, -1, -1):
        day = now().date() - timedelta(days=i)

        total = Attendance.objects.filter(
            student__instructorstudent__instructor=instructor,
            date=day
        ).count()

        present = Attendance.objects.filter(
            student__instructorstudent__instructor=instructor,
            date=day,
            present=True
        ).count()

        percent = round((present / total) * 100) if total else 0

        attendance_labels.append(day.strftime('%a'))
        attendance_trend.append(percent)

    practice_labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    practice_trend = []

    today = now().date()
    start_of_this_week = today - timedelta(days=today.weekday())

    for i in range(3, -1, -1):
        week_start = start_of_this_week - timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)

        avg = (
            PracticeLog.objects.filter(
                student__instructorstudent__instructor=instructor,
                date__range=(week_start, week_end)
            ).aggregate(avg=Avg('hours'))['avg']
        ) or 0

        practice_trend.append(round(float(avg), 1))

    ai_qs = AIInsight.objects.filter(
        student__instructorstudent__instructor=instructor
    )

    needs_attention = ai_qs.filter(cluster=2).count()
    total_ai = ai_qs.count()

    if total_ai == 0:
        ai_insight = "AI analysis pending"
    elif needs_attention > 0:
        ai_insight = "Some students need additional attention"
    else:
        ai_insight = "Overall student progress is stable"

    context = {
        'total_students': students.count(),
        'avg_practice': avg_practice,
        'ai_insight': ai_insight,
        'discipline_level': 'Stable',

        'attendance_labels': attendance_labels,
        'attendance_trend': attendance_trend,

        'practice_labels': practice_labels,
        'practice_trend': practice_trend,

        'documents': LearningDocument.objects.filter(instructor=instructor),

        'instructor_name': instructor.user.get_full_name() or instructor.user.username,
        'instructor_email': instructor.user.email,
    }

    return render(request, 'instructors/dashboard.html', context)

@login_required
def daily_activity(request):
    instructor = get_object_or_404(InstructorProfile, user=request.user)

    if request.method == 'POST':
        form = DailyActivityForm(request.POST, instructor=instructor)

        if form.is_valid():
            student = form.cleaned_data['student']
            activity_date = form.cleaned_data['date']
            is_present = form.cleaned_data['is_present']
            hours = form.cleaned_data['hours']

            if activity_date > date.today():
                return redirect('daily_activity')

            Attendance.objects.update_or_create(
                student=student,
                date=activity_date,
                defaults={'present': is_present}
            )

            log, created = PracticeLog.objects.get_or_create(
                student=student,
                date=activity_date,
                defaults={'hours': hours}
            )

            if not created:
                log.hours = float(log.hours) + float(hours)
                log.save()

            return redirect('instructor_dashboard')
    else:
        form = DailyActivityForm(instructor=instructor)

    return render(
        request,
        'instructors/daily_activity.html',
        {'form': form}
    )

@login_required
def instructor_students(request):
    instructor = get_object_or_404(InstructorProfile, user=request.user)

    today = now().date()
    month_start = today.replace(day=1)

    mappings = InstructorStudent.objects.filter(
        instructor=instructor
    ).select_related('student__user')

    students_data = []

    for m in mappings:
        student = m.student
        total_days = Attendance.objects.filter(
            student=student,
            date__range=(month_start, today)
        ).count()

        present_days = Attendance.objects.filter(
            student=student,
            date__range=(month_start, today),
            present=True
        ).count()

        attendance_percent = (
            round((present_days / total_days) * 100)
            if total_days else 0
        )

        monthly_practice = (
            PracticeLog.objects.filter(
                student=student,
                date__range=(month_start, today)
            ).aggregate(total=Sum('hours'))['total']
        ) or 0

        monthly_practice = float(monthly_practice)

        avg_weekly_practice = monthly_practice / 4 if monthly_practice else 0
        practice_score = min((avg_weekly_practice / 5) * 100, 100)

        progress_score = round(
            (attendance_percent * 0.6) +
            (practice_score * 0.4)
        )

        students_data.append({
            'student': student,
            'attendance_percent': attendance_percent,
            'monthly_practice': monthly_practice,
            'progress_score': progress_score,
        })

    return render(
        request,
        'instructors/student_list.html',
        {'students_data': students_data}
    )

@login_required
def attendance_history(request):
    instructor = get_object_or_404(InstructorProfile, user=request.user)

    records = Attendance.objects.filter(
        student__instructorstudent__instructor=instructor
    ).order_by('-date')

    return render(
        request,
        'instructors/attendance_history.html',
        {'records': records}
    )

@login_required
def upload_document(request):
    instructor = get_object_or_404(InstructorProfile, user=request.user)

    if request.method == 'POST':
        form = LearningDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.instructor = instructor
            document.save()
            return redirect('instructor_dashboard')
    else:
        form = LearningDocumentForm()

    return render(
        request,
        'instructors/upload_document.html',
        {'form': form}
    )

@login_required
def delete_document(request, doc_id):
    instructor = get_object_or_404(InstructorProfile, user=request.user)

    document = get_object_or_404(
        LearningDocument,
        id=doc_id,
        instructor=instructor
    )
    document.delete()

    return redirect('instructor_dashboard')
