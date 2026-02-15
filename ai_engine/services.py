import numpy as np
from sklearn.cluster import KMeans
from django.db.models import Avg
from students.models import StudentProfile
from instructors.models import Attendance, PracticeLog
from .models import AIInsight


def run_ai_analysis():
    students = StudentProfile.objects.all()

    data = []
    student_map = []

    for student in students:
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, present=True).count()
        attendance_pct = (present / total) * 100 if total else 0

        avg_practice = (
            PracticeLog.objects
            .filter(student=student)
            .aggregate(avg=Avg('hours'))['avg']
        ) or 0

        data.append([attendance_pct, float(avg_practice)])
        student_map.append(student)

    n_samples = len(data)
    
    if n_samples < 2:
        return  
    n_clusters = min(3, n_samples)

    X = np.array(data)

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X)

    for student, label in zip(student_map, labels):

        if label == 0:
            status = "Improving"
            message = (
                "Your performance is improving. Maintain attendance "
                "and increase practice consistency."
            )

        elif label == 1:
            status = "Stable"
            message = (
                "Your progress is stable. Increasing daily practice "
                "will help you improve faster."
            )

        else:
            status = "Needs Attention"
            message = (
                "Irregular attendance or practice detected. "
                "Focus on building a consistent routine."
            )

        AIInsight.objects.update_or_create(
            student=student,
            defaults={
                'cluster': int(label),
                'status': status,
                'message': message
            }
        )
